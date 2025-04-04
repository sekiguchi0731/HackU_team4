from typing import Literal
from flask import render_template, request, jsonify
from flask_cors import cross_origin
from werkzeug.datastructures.structures import ImmutableMultiDict
from hackapp import app,db
from .models.restaurants import User,Shop,Seat
from datetime import datetime
import utils
import json
from flask import Response
def load_data():
    with open('restaurants.json', 'r', encoding='utf-8') as f:
        return json.load(f)
from urllib.parse import quote  # ←これ追加
import random

@app.route("/recommend", methods=["GET"])
def recommend():
    user_lat = request.args.get("user_lat", type=float)
    user_lng = request.args.get("user_lng", type=float)
    user_pos = request.args.get("user_pos", type=str)
    preferred_category = request.args.get("preferred_category", type=str, default="")
    current_time = request.args.get("current_time", type=str)

    if (user_lat is None or user_lng is None) and not user_pos:
        return jsonify({"error": "位置情報（緯度経度）または住所が必要です"}), 400
    if not current_time:
        return jsonify({"error": "現在時刻が必要です"}), 400

    if user_lat is not None and user_lng is not None:
        user_location = (user_lat, user_lng)
        print(f"緯度経度で受信: 緯度={user_lat}, 経度={user_lng}")
    else:
        user_location = user_pos
        print(f"住所で受信: {user_pos}")

    print(f"希望カテゴリ: {preferred_category}")
    print(f"現在時刻: {current_time}")

    recommendations = utils.recommend_shops(user_location, preferred_category, current_time)
    images = utils.get_pixabay_cropped_images(preferred_category, num_images=10,width=300,height=200)
    formatted_recommendations = [
        {
            "id": index + 1,
            "name": rec["name"],
            "description": (
                f"距離スコア: {rec['distance']:.2f}, "
                f"空席数: {rec['total_available_capacity']}, "
            ),
            "image": random.choice(images) if images else "https://via.placeholder.com/300x200?text=No+Image"

            
        }
        for index, rec in enumerate(recommendations)
    ]

    response = json.dumps({"recommendations": formatted_recommendations}, ensure_ascii=False)
    print(f"レスポンス: {response}")
    return Response(response, content_type="application/json; charset=utf-8")

@app.route('/recomend')
def recomend_page():
    return render_template('recomend.html')

@app.route('/') #初期画面
def index():
    return render_template('index.html')

@app.route('/users_sign_up')    #ユーザ登録画面
def users_sign_up():
    return render_template('users.html')

@app.route("/signed_up", methods=["POST"])
def signed_up() -> Response:
    data: dict[str, str] = request.get_json()
    user = User(
        id=len(User.query.all()) + 1,
        name=data["name"],
        email=data["email"],
        password=data["password"],
        role=data["role"],
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"status": "ok", "message": "ユーザー登録完了"})

@app.route('/users', methods=['GET', 'POST'])   #ユーザ登録画面から受け取ったパラメータをDBに登録した後に一覧表示する画面
def create_users():
    users = User.query.all()
    if request.method == 'POST':
        data = request.form
        user = User(
            id = len(users) + 1,
            name = data['name'],
            email = data['email'],
            password = data['password'],  # 実際はハッシュ化する
            role = data['role'],
            created_at = datetime.now(),
            updated_at = datetime.now()
        )
        db.session.add(user)
        db.session.commit()

    # HTMLページとしてユーザーリストを表示
    return render_template('users_view.html', users=users)

@app.route('/sign_in')  #ログイン画面
def sign_in():
    return render_template('sign_in.html')

@app.route('/signed_in', methods=['POST'])  # ログイン後の画面、ログイン失敗、お客、店主の3パターンからなる
def signed_in() -> Response | tuple[Response, Literal[401]]:
    data: dict[str, str] = request.get_json()
    email: str | None = data.get("email")
    password: str | None = data.get("password")

    user: User | None = User.query.filter_by(email=email, password=password).first()
    if user:
        if user.role == "お客":
            return jsonify({"status": "ok", "role": "customer", "email": email})
        else:
            return jsonify({"status": "ok", "role": "owner", "owner_id": user.id})
    else:
        return jsonify({"status": "error", "message": "ログイン失敗"}), 401


@app.route('/debug_signed_in', methods=['POST'])  # ログイン後の画面、ログイン失敗、お客、店主の3パターンからなる
def debug_signed_in():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email, password=password).first()
    if user:
        if user.role == "お客":
            return render_template('search.html', emeil=email, password=password)
        else:
            return render_template('owner_select.html',owner_id = user.id)
    else:
        return render_template('sign_in_failed.html')


@app.route('/shops_sign_up', methods=['GET','POST'])    #お店の登録画面
def shops_sign_up():
    id = request.form.get("owner_id")
    return render_template('shops.html',owner_id = id)

@app.route('/shops', methods=['GET','POST'])    #お店登録画面から受け取った情報をDBに保存&表示
def create_shop():

    id = request.form.get("owner_id")
    shops=Shop.query.all()
    if request.method == 'POST':
        data = request.form
        shop=Shop(
            id = len(shops) + 1,
            name = data['name'],
            address = data['address'],
            phone = data['phone'],
            category = data['category'],
            opening_time = data['opening_time'],
            closing_time = data['closing_time'],
            owner_id = id,
            created_at = datetime.now(),
            updated_at = datetime.now()
        )
        db.session.add(shop)
        db.session.commit()

    return render_template('shops_view.html', shops=shops)

# shopの有無を確認するAPI
@app.route("/owner/<int:owner_id>/check_shop", methods=["GET"])
def check_owner_shop(owner_id) -> Response:
    shop = Shop.query.filter_by(owner_id=owner_id).first()

    if shop:
        return jsonify({"has_shop": True, "shop_id": shop.id})
    else:
        return jsonify({"has_shop": False})

# owner_idからshop_idを取得するAPI
@app.route("/shops_by_owner/<int:owner_id>")
def get_shops_by_owner(owner_id) -> tuple[Response, Literal[404]] | Response:
    shops: list = Shop.query.filter_by(owner_id=owner_id).all()

    if not shops:
        return jsonify({"error": "店舗が見つかりません"})

    return jsonify(
        {
            "shops": [
                {
                    "id": shop.id,
                    "name": shop.name,
                    "address": shop.address,
                    "category": shop.category,
                    "phone": shop.phone,
                }
                for shop in shops
            ]
        }
    )


@app.route('/seats_sign_up',methods=['GET','POST'])    #空席情報登録画面   
def seats_sign_up():
    id = request.form.get("owner_id")
    return render_template('seats.html',owner_id = id)

@app.route('/seats_delete', methods=['POST'])
def seats_delete():
    # フォームからオーナーIDを取得
    owner_id = request.form.get("owner_id")
    
    # オーナーIDに紐付く全店舗を取得
    shops = Shop.query.filter_by(owner_id=owner_id).all()
    
    if not shops:  # 店舗が見つからない場合
        return render_template("error.html", message="指定されたオーナーに関連する店舗が見つかりません。")
    
    # 店舗IDに紐付くすべての座席情報を取得
    seats = Seat.query.filter(Seat.shop_id.in_([shop.id for shop in shops]), Seat.is_active.is_(True)).all()
    
    if not seats:  # 座席が見つからない場合
        return render_template("error.html", message="指定されたオーナーに関連する座席が見つかりません。")
    
    # テンプレートにデータを渡してレンダリング
    return render_template('seats_delete.html', shops=shops, seats=seats)

@app.route('/seats_delete_confirm', methods=['POST'])
def seats_delete_confirm():
    # フォームデータから座席IDを取得
    seat_id = request.form.get("seat_id")

    if not seat_id:
        return render_template("error.html", message="座席IDが指定されていません。")

    # 指定された座席情報を取得
    seat = Seat.query.get(seat_id)
    if not seat:
        return render_template("error.html", message="指定された座席が見つかりません。")

    # 座席のis_activeをFalseに設定して削除を実現
    seat.is_active = False
    try:
        db.session.commit()  # データベースに変更を保存
    except Exception as e:
        db.session.rollback()
        return render_template("error.html", message="座席を削除する際にエラーが発生しました。")

    # 削除完了ページを表示
    return render_template("seats_delete_success.html", message=f"座席ID {seat_id} を削除しました。")

@app.route('/activate_all_seats', methods=['POST']) #デバッグ用、押すと全seatのis_activeがTrueになります。
def activate_all_seats():
    try:
        # すべての座席を取得
        seats = Seat.query.all()
        
        if not seats:  # 座席が見つからない場合
            return jsonify({"message": "座席データが存在しません"}), 404
        
        # 各座席のis_activeをTrueに設定
        for seat in seats:
            seat.is_active = True
        
        # データベースに変更を保存
        db.session.commit()

        return jsonify({"message": "すべての座席を有効化しました"}), 200

    except Exception as e:
        # エラーが発生した場合はロールバック
        db.session.rollback()
        return jsonify({"message": "エラーが発生しました", "error": str(e)}), 500
    
@app.route('/seats', methods=['GET','POST'])    #空席情報登録画面から受け取った情報をDBに格納&表示
def create_seat():
    if request.method == 'GET':
        seats = Seat.query.all()
        return render_template('seats_view.html', seats=seats)
    
    if request.method == 'POST':
        data = request.form
        # 名前とオーナーIDを基にShopテーブルから店舗を取得
        shop = Shop.query.filter_by(name=data['shop_name'], owner_id=data['owner_id']).first()
        
        if shop:  # 店舗が存在する場合
            # 新しい席情報を登録
            seat = Seat(
                shop_id=shop.id,
                name=data['name'],
                capacity=data['capacity'],
            )
            db.session.add(seat)
            db.session.commit()

            # 最新のデータを取得して表示
            seats = Seat.query.all()
            return render_template('seats_view.html', seats=seats)
        
        else:  # 店舗が存在しない場合
            return render_template('seats_failed.html', message="指定された店舗またはオーナーが一致しませんでした。")

@app.route('/seats_register', methods=['POST'])    #空席情報登録画面から受け取った情報をDBに格納&表示
def register_seat() -> tuple[Response, Literal[400]] | Response | tuple[Response, Literal[404]]:
    data: ImmutableMultiDict[str, str] = request.form
    shop_id: str | None = data.get("shop_id")
    if not shop_id:
        return jsonify({"error": "shop_idが必要です"}), 400

    shop = Shop.query.get(shop_id)
    if shop:
        seat = Seat(
            shop_id=shop.id,
            name=data["name"],
            capacity=data["capacity"],
        )
        db.session.add(seat)
        db.session.commit()
        return jsonify({"status": "ok", "message": "席を登録しました"})
    else:
        return jsonify({"status": "error", "message": "ショップが見つかりません"}), 404

@app.route('/register') #お店登録画面（削除予定）
def register():
    return render_template('register.html')

@app.route('/regi_end', methods=['POST'])   #削除予定
def reg_end():
    area = request.form.get('area')
    genre = request.form.get('genre')
    
    return render_template('regi_end.html', area=area, genre=genre)


@app.route('/search')   #お店検索画面
def search():
    return render_template('search.html')

# 全てのジャンルを取得する
@app.route("/genres", methods=["GET"])
@cross_origin(origins="http://localhost:5173")
def get_genres() -> Response:
    genres = db.session.query(Shop.category).distinct().all()
    genre_list = [g[0] for g in genres if g[0]]  # タプルから文字列を取り出す
    return jsonify(genre_list)


@app.route('/result', methods=['POST']) #検索したお店を表示する画面
def result():
    genre = request.form.get('genre')
    address = request.form.get('address')

    data = load_data()

    #観測地からの距離を測定
    for shop in data:
        shop["distance"] = utils.make_dis(address,shop["address"])

    # フィルタリング
    results = [shop for shop in data if
               (genre.lower() in shop['genre'].lower()) and
               shop['seats_available'] > 0 and shop['distance'] < 50]
    
    return render_template('results.html', results=results, genre=genre)


@app.route('/reserve', methods=['GET', 'POST'])
def reserve_page():
    if request.method == 'GET':
        # クエリパラメータからショップ名を取得
        shop_name = request.args.get("shop_name", "不明なショップ")

        # ショップ名に基づいて店舗を取得
        shop = Shop.query.filter_by(name=shop_name).first()

        if not shop:
            return render_template("reserve.html", shop_name=shop_name, seats=[])

        # 該当店舗の is_active=True の席を取得
        active_seats = Seat.query.filter_by(shop_id=shop.id, is_active=True).all()

        # 席情報をテンプレートに渡す
        return render_template("reserve.html", shop_name=shop_name, seats=active_seats)

    elif request.method == 'POST':
        # フォームデータから選択された席のIDを取得
        seat_id = request.form.get("seat_id")
        shop_name = request.form.get("shop_name")

        if not seat_id:
            return render_template("reserve.html", shop_name=shop_name, seats=[], error="席を選択してください。")

        # 選択された席を予約（is_active を False に変更）
        seat = Seat.query.get(seat_id)
        if seat and seat.is_active:
            seat.is_active = False
            #testのためいちいちfalseにするとめんどくさいのでのちにコメントアウト#
            seat.is_active = True

            db.session.commit()
            return render_template("reserve_success.html", shop_name=shop_name, seat=seat)
        else:
            return render_template("reserve.html", shop_name=shop_name, seats=[], error="選択された席が見つからないか、既に予約されています。")