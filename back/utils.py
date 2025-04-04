import requests
import urllib
import re
from geopy.distance import geodesic
from datetime import datetime  # datetimeをインポート
from sqlalchemy import and_, exists, select, func
from hackapp import app,db
# データベースモデルのインポート
from hackapp.models.restaurants import User,Shop,Seat
from geopy.distance import geodesic

import requests
import urllib.parse
import re
from geopy.distance import geodesic
import logging
#経度，緯度の情報をもらう
def make_dis(pos1, pos2): 
    makeUrl = "https://msearch.gsi.go.jp/address-search/AddressSearch?q="

    # 座標取得ヘルパー
    def get_coordinates(pos):
        # posがタプル（緯度・経度）ならそのまま返す
        if isinstance(pos, (tuple, list)) and len(pos) == 2:
            lat, lng = pos
            return lng, lat  # 緯度経度 → 経度緯度に変換

        # posが文字列（住所）の場合はジオコーディング
        s_quote = urllib.parse.quote(pos)
        response = requests.get(makeUrl + s_quote)
        try:
            data = response.json()
        except ValueError:
            print(f"レスポンスをJSONとしてパースできませんでした: {pos}")
            return None
        
        if not data:
            print(f"APIからデータが返ってきませんでした: {pos}")
            return None
        
        try:
            longitude, latitude = data[0]["geometry"]["coordinates"]
            return longitude, latitude
        except (IndexError, KeyError) as e:
            print(f"座標取得中にエラーが発生しました ({pos}): {e}")
            return None

    # 座標取得
    coord1 = get_coordinates(pos1)
    coord2 = get_coordinates(pos2)

    if coord1 is None or coord2 is None:
        return None

    # 座標（経度緯度）→ geodesic の引数（緯度, 経度）形式に変換
    lon1, lat1 = coord1
    lon2, lat2 = coord2
    print("user_pos:", coord1)
    # 距離計算
    distance = geodesic((lat1, lon1), (lat2, lon2))

    # 数値だけ抽出して四捨五入（小数1桁）
    match = re.search(r"[+-]?(?:\d+\.\d*|\.\d+|\d+\.)", str(distance))
    if match:
        num = round(float(match.group()), 1)
        return num
    else:
        print("距離の数値を抽出できませんでした。")
        return None


from datetime import datetime
from sqlalchemy import and_, exists

def recommend_shops(user_pos, preferred_category, current_time):
    current_time = datetime.strptime(current_time, "%H:%M").time()
    current_time_str = current_time.strftime("%H:%M")

    print("debug: current_time:", current_time)
    print("debug: user_pos:", user_pos)

    # ShopとSeatをJOINして、空席数(capacity合計)をGROUP BYで計算
    results = db.session.query(
        Shop.id,
        Shop.name,
        Shop.address,
        func.sum(Seat.capacity).label("total_available_capacity")
    ).join(Seat, Shop.id == Seat.shop_id
    ).filter(
        and_(
            Shop.category == preferred_category,
            Shop.opening_time <= current_time_str,
            Shop.closing_time >= current_time_str,
            Seat.is_active == True,
            Seat.capacity > 0
        )
    ).group_by(Shop.id).all()

    print("debug: filtered_shops with capacity sum:", results)

    recommendations = []

    for shop_id, name, address, total_capacity in results:
        if not address:
            print(f"Shop {name} is missing an address.")
            continue

        shop_distance = make_dis(user_pos, address)
        if shop_distance is None:
            print(f"Could not calculate distance for shop {name}.")
            continue

        recommendations.append({
            "shop_id": shop_id,
            "name": name,
            "distance": shop_distance,
            "total_available_capacity": total_capacity
        })

    recommendations.sort(key=lambda x: x["distance"])
    print("debug: recommendations:", recommendations)
    return recommendations

pos1='石川県金沢市もりの里1丁目45-1'
pos2='千葉県南房総市富浦町青木123-1'

num=make_dis(pos1,pos2)
print(num)
