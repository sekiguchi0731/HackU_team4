from flask import render_template, request, jsonify
from hackapp import app,db
from .models.restaurants import User,Shop,Seat
from datetime import datetime
import utils
import json

def load_data():
    with open('restaurants.json', 'r', encoding='utf-8') as f:
        return json.load(f)


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
            genre = data['genre'],
            opening_time = data['opening_time'],
            closing_time = data['closing_time'],
            owner_id = id,
            created_at = datetime.now(),
            updated_at = datetime.now()
        )
        db.session.add(shop)
        db.session.commit()

    return render_template('shops_view.html', shops=shops)

@app.route('/seats_sign_up')    #空席情報登録画面   
def seats_sign_up():
    return render_template('seats.html')

@app.route('/seats', methods=['GET','POST'])    #空席情報登録画面から受け取った情報をDBに格納&表示
def create_seat():
    seats = Seat.query.all()
    if request.method == 'POST':
        data = request.form
        seat = Seat(
            id = len(seats) + 1,
            shop_id = data['shop_id'],
            name = data['name'],
            capacity = data['capacity'],
        )
        db.session.add(seat)
        db.session.commit()
    return render_template('seats_view.html', seats=seats)

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
    


    return render_template('results.html', results=results, genre=genre,)