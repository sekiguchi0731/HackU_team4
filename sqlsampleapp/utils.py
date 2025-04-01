import requests
import urllib
import re
from geopy.distance import geodesic
from datetime import datetime  # datetimeをインポート
from sqlalchemy import and_  # SQLAlchemyのand_をインポート
from hackapp import app,db
# データベースモデルのインポート
from hackapp.models.restaurants import User,Shop,Seat
from geopy.distance import geodesic

def make_dis(pos1, pos2):
    makeUrl = "https://msearch.gsi.go.jp/address-search/AddressSearch?q="
    
    # 座標取得用のヘルパー関数
    def get_coordinates(pos):
        s_quote = urllib.parse.quote(pos)
        response = requests.get(makeUrl + s_quote)
        try:
            data = response.json()
        except ValueError:
            print(f"レスポンスをJSONとしてパースできませんでした: {pos}")
            return None
        
        # レスポンスが空の場合
        if not data:
            #print(f"APIからデータが返ってきませんでした: {pos}")
            return None
        
        try:
            # 最初の結果から座標を取得
            longitude, latitude = data[0]["geometry"]["coordinates"]
            return longitude, latitude
        except (IndexError, KeyError) as e:
            print(f"座標取得中にエラーが発生しました ({pos}): {e}")
            return None

    # pos1の座標取得
    coord1 = get_coordinates(pos1)
    if coord1 is None:
        return None
    # pos2の座標取得
    coord2 = get_coordinates(pos2)
    if coord2 is None:
        return None

    longitude1, latitude1 = coord1
    longitude2, latitude2 = coord2

    # 距離の計算
    distance = geodesic((latitude1, longitude1), (latitude2, longitude2))
    
    # 距離オブジェクトから数値部分を抽出して四捨五入（1桁）
    match = re.search(r"[+-]?(?:\d+\.\d*|\.\d+|\d+\.)", str(distance))
    if match:
        num = round(float(match.group()), 1)
        return num
    else:
        print("距離の数値を抽出できませんでした。")
        return None
def recommend_shops(user_lat, user_lng, preferred_category, current_time):
    # 現在の時刻をdatetimeオブジェクトに変換
    current_time = datetime.strptime(current_time, "%H:%M").time()

    # データベースからショップ情報を取得
    shops = db.session.query(Shop).all()
    recommendations = []
    pos2='千葉県南房総市富浦町青木123-1'
    for shop in shops:
        # 距離スコア
        if not shop.address:
            print(f"Shop {shop.name} is missing an address.")
            continue

        shop_distance = make_dis(pos2, shop.address)

        if shop_distance is None:
            print(f"Could not calculate distance for shop {shop.name}.")
            continue

        # 10km以内なら線形にスコア、10km以上は0
        distance_score = max(0, 1 - shop_distance / 10)
        # カテゴリスコア
        category_score = 1.0 if hasattr(shop, 'category') and shop.category == preferred_category else 0.0

        # 営業時間スコア
        try:
            opening_time = datetime.strptime(shop.opening_time, "%H:%M").time()
            closing_time = datetime.strptime(shop.closing_time, "%H:%M").time()
            time_score = 1.0 if opening_time <= current_time <= closing_time else 0.0
        except ValueError:
            print(f"Invalid time format for shop {shop.name}.")
            time_score = 0.0

        # 空席スコア
        seats = db.session.query(Seat).filter(
            and_(Seat.shop_id == shop.id, Seat.is_active == True)
        ).all()
        seat_score = 1.0 if any(seat.capacity > 0 for seat in seats) else 0.0

        # 総合スコア（重みを調整可能）
        total_score = (
            0.4 * distance_score +
            0.3 * category_score +
            0.2 * time_score +
            0.1 * seat_score
        )

        if total_score > 0:
            recommendations.append((shop.name, f"totalscore_{total_score}",f"categoryscore_{category_score}",f"distancescore_{distance_score}", f"timescore_{time_score}", f"seatscore_{seat_score}"))

    # スコア順にソート
    recommendations.sort(key=lambda x: x[1], reverse=True)
    return recommendations

pos1='石川県金沢市もりの里1丁目45-1'
pos2='千葉県南房総市富浦町青木123-1'

num=make_dis(pos1,pos2)
print(num)
