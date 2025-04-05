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
import requests
from PIL import Image
from io import BytesIO
from urllib.parse import quote
import base64
from datetime import datetime
from sqlalchemy import and_, exists
#経度，緯度の情報をもらう
def make_dis(pos1, pos2): 
    makeUrl = "https://msearch.gsi.go.jp/address-search/AddressSearch?q="

    def get_coordinates(pos):
        if isinstance(pos, (tuple, list)) and len(pos) == 2:
            lat, lng = pos
            return lng, lat
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

    coord1 = get_coordinates(pos1)
    coord2 = get_coordinates(pos2)

    if coord1 is None or coord2 is None:
        return None

    lon1, lat1 = coord1
    lon2, lat2 = coord2

    # 距離計算（km単位）
    distance_km = geodesic((lat1, lon1), (lat2, lon2)).km
    rounded_distance = round(distance_km, 1)

    # 徒歩時間（分）＝ 距離[km] ÷ 4.8[km/h] × 60[min]
    walk_time_min = round((distance_km / 4.8) * 60)

    return {
        "distance_km": rounded_distance,
        "walk_minutes": walk_time_min
    }





# SQLがDATA型ではないため苦肉の策
def is_open(opening_str, closing_str, current_time):
    try:
        opening = datetime.strptime(opening_str, "%H:%M").time()
        closing = datetime.strptime(closing_str, "%H:%M").time()
    except ValueError:
        return False

    if opening < closing:
        return opening <= current_time <= closing
    else:
        # 例：20:00〜02:00 のような深夜営業に対応
        return current_time >= opening or current_time <= closing
import random
from urllib.parse import quote


def get_pixabay_cropped_images(query: str, num_images: int = 5, width: int = 300, height: int = 200) -> list[str]:
    """
    Pixabayから画像を検索し、指定サイズにトリミングして、base64形式で返す
    """
    API_KEY = "49651736-8789044e12cc0944b118087dd"
    query_encoded = quote(query)
    url = (
        f"https://pixabay.com/api/"
        f"?key={API_KEY}"
        f"&q={query_encoded}"
        f"&image_type=photo"
        f"&per_page={num_images}"
        f"&safesearch=true"
    )

    try:
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        if res.status_code != 200:
            print("Pixabay APIエラー:", res.status_code)
            return []

        data = res.json()
        hits = data.get("hits", [])
        image_urls = [img["webformatURL"] for img in hits]

        # 取得した画像URLをリサイズしてbase64で返す
        cropped_images_base64 = []
        for url in image_urls:
            img = download_and_crop_image(url, width, height)
            if img:
                base64_img = encode_image_to_base64(img)
                cropped_images_base64.append(base64_img)

        return cropped_images_base64

    except Exception as e:
        print("画像取得失敗:", e)
        return []

def download_and_crop_image(url: str, width: int = 300, height: int = 200) -> Image.Image:
    """
    URLから画像をダウンロードし、指定サイズにリサイズ（中央トリミング）
    """
    try:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content)).convert("RGB")

        # アスペクト比無視でサイズ変更（中央クロップしたいなら別ロジックも可能）
        img = img.resize((width, height), Image.LANCZOS)
        return img
    except Exception as e:
        print("画像処理エラー:", e)
        return None

def encode_image_to_base64(img: Image.Image) -> str:
    """
    Pillow画像をbase64エンコードしてdata URLにする
    """
    buffer = BytesIO()
    img.save(buffer, format="JPEG")
    encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return f"data:image/jpeg;base64,{encoded}"
def recommend_shops(user_pos, preferred_category, current_time):
    current_time_obj = datetime.strptime(current_time, "%H:%M").time()

    results = db.session.query(
        Shop.id,
        Shop.name,
        Shop.address,
        Shop.opening_time,
        Shop.closing_time,
        Shop.category,
        func.sum(Seat.capacity).label("total_available_capacity")
    ).join(Seat, Shop.id == Seat.shop_id
    ).filter(
        and_(
            Shop.category == preferred_category,
            Seat.is_active == True,
            Seat.capacity > 0
        )
    ).group_by(Shop.id).all()

    recommendations = []

    for shop_id, name, address, opening_time, closing_time, category, total_capacity in results:
        if not address:
            continue
        if not is_open(opening_time, closing_time, current_time_obj):
            continue

        shop_distance_info = make_dis(user_pos, address)
        if shop_distance_info is None:
            continue

        recommendations.append({
            "shop_id": shop_id,
            "name": name,
            "address": address,
            "distance": shop_distance_info["distance_km"],
            "walk_minutes": shop_distance_info["walk_minutes"],
            "total_available_capacity": total_capacity,
            "category": category,
            "opening_time": opening_time,
            "closing_time": closing_time
        })

    recommendations.sort(key=lambda x: x["distance"])
    return recommendations
pos1='石川県金沢市もりの里1丁目45-1'
pos2='千葉県南房総市富浦町青木123-1'

num=make_dis(pos1,pos2)
print(num)