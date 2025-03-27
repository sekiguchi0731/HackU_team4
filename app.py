from flask import Flask, render_template, jsonify, request
import random
import json

app = Flask(__name__)

# 店舗データ（例としてのJSON）
restaurants = [
    {"name": "ラーメン王", "genre": "ラーメン", "price_range": "中価格", "rating": 4.5, "location": "大宮市北区"},
    {"name": "寿司大", "genre": "寿司", "price_range": "高価格", "rating": 4.7, "location": "東京都港区"},
    {"name": "居酒屋あさり", "genre": "居酒屋", "price_range": "安価", "rating": 3.8, "location": "大阪市"},
    # 他の店舗も追加可能
]

@app.route("/")
def home():
    return render_template("index.html")  # フロントエンドHTMLを表示

# 飲食店情報をジャンルに基づいて表示するページ
@app.route('/restaurant')
def restaurant():
    genre = request.args.get('genre')
    if genre is None:
        return jsonify({"error": "ジャンルが選択されていません"}), 400

    # ジャンルに一致するレストランをフィルタリング
    filtered_restaurants = [r for r in restaurants if r['genre'] == genre]

    if not filtered_restaurants:
        return render_template('error.html', error_message="該当するお店が見つかりませんでした。")

    # ランダムで1軒のレストランを返す
    restaurant = random.choice(filtered_restaurants)
    return render_template('restaurant.html', restaurant=restaurant, genre=genre)

# ジャンルを指定して店舗をランダムに返すエンドポイント
@app.route("/random_by_genre", methods=["GET"])
def get_random_by_genre():
    genre = request.args.get("genre")  # クエリパラメータとしてジャンルを取得
    
    if not genre:
        return jsonify({"error": "ジャンルが指定されていません"}), 400
    
    # ジャンルでフィルタリング
    filtered_restaurants = [r for r in restaurants if r["genre"] == genre]
    
    if not filtered_restaurants:
        return render_template('error.html', error_message="該当するお店が見つかりませんでした。")
        
    # ランダムに1件を選んで返す
    random_restaurant = random.choice(filtered_restaurants)
    return jsonify(random_restaurant)

# if __name__ == "__main__":
#     app.run(debug=True, host="127.0.0.1", port=5000)

if __name__ == '__main__':
    app.run(debug=True)
