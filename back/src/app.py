from flask import Flask, jsonify, request
import json
import os
import random
app = Flask(__name__)
DATA_FILE = "../data/tenmpo_data.json"


@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <title>飲食店データベース</title>
        <style>
            body { font-family: sans-serif; padding: 2rem; background: #f8f8f8; }
            h1 { color: #333; }
            button {
                padding: 10px 20px;
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
            }
            button:hover {
                background-color: #0056b3;
            }
            #result {
                margin-top: 20px;
                font-size: 18px;
                color: #222;
            }
        </style>
    </head>
    <body>
        <h1>🍽 飲食店データベース API</h1>
        <p>以下のボタンを押す.データベースに入っている店名をランダムに返します．</p>
        <button onclick="fetchRandomRestaurant()">ランダムなお店を取得</button>
        <div id="result"></div>

        <script>
            function fetchRandomRestaurant() {
                fetch('/restaurant/random')
                    .then(response => response.json())
                    .then(data => {
                        if (data["店名"]) {
                            document.getElementById("result").innerText = "店名: " + data["店名"];
                        } else {
                            document.getElementById("result").innerText = "お店が見つかりません。";
                        }
                    })
                    .catch(error => {
                        document.getElementById("result").innerText = "エラーが発生しました。";
                        console.error(error);
                    });
            }
        </script>    
    </body>
</html>
'''



# 初期データをロード
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for i, item in enumerate(data):
                item["id"] = i + 1
            return data
    return []

restaurants = load_data()

# 保存用（任意：永続化したい場合に呼ぶ）
def save_data():
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(restaurants, f, ensure_ascii=False, indent=2)

# 1. お店を単体で返す関数
@app.route('/restaurant/random', methods=['GET'])
def get_random_restaurant():
    if not restaurants:
        return jsonify({"error": "レストランデータが空です"}), 404
    restaurant = random.choice(restaurants)
    return jsonify(restaurant)


# 2. お店をリスト化して複数返す関数
@app.route('/restaurants', methods=['GET'])
def get_all_restaurants():
    return jsonify(restaurants)

# 3. お店を追加する関数
@app.route('/restaurant', methods=['POST'])
def add_restaurant():
    new_data = request.json
    if not new_data.get("店名") or not new_data.get("ジャンル") or not new_data.get("席数"):
        return jsonify({"error": "必要な情報が不足しています"}), 400

    new_data["id"] = max([r["id"] for r in restaurants], default=0) + 1
    new_data["予約数"] = 0
    restaurants.append(new_data)
    save_data()
    return jsonify(new_data), 201

if __name__ == '__main__':
    app.run(debug=True)
