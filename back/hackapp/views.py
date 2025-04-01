from flask import render_template, request, jsonify
from flask_cors import cross_origin
from hackapp import app,db
from .models.restaurants import User,Shop,Seat
from datetime import datetime
import utils
import json
from flask import Response
def load_data():
    with open('restaurants.json', 'r', encoding='utf-8') as f:
        return json.load(f)

@app.route("/recommend", methods=["GET"])
def recommend():
    """
    ユーザーの位置情報、希望カテゴリ、現在時刻を受け取り、ショップを推薦するエンドポイント
    """
    # クエリパラメータを取得
    user_lat = request.args.get("user_lat", type=float)
    user_lng = request.args.get("user_lng", type=float)
    preferred_category = request.args.get("preferred_category", type=str, default="")
    current_time = request.args.get("current_time", type=str)

    # 必須パラメータのチェック
    if user_lat is None or user_lng is None or current_time is None:
        return jsonify({"error": "Missing required parameters"}), 400

    # recommend_shops 関数を呼び出し
    recommendations = utils.recommend_shops(user_lat, user_lng, preferred_category, current_time)
    response = json.dumps({"recommendations": recommendations}, ensure_ascii=False)
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

@app.route('/signed_in', methods=['POST'])  #ログイン後の画面、ログイン失敗、お客、店主の3パターンからなる
def signed_in():
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

@app.route('/seats_sign_up',methods=['GET','POST'])    #空席情報登録画面   
def seats_sign_up():
    id = request.form.get("owner_id")
    return render_template('seats.html',owner_id = id)

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