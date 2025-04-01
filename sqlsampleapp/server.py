from hackapp import app,db

if __name__ == "__main__":
    app.run()

"""
以下実行でデータベース作成できます。
with app.app_context():  # アプリケーションコンテキストを作成
    db.create_all()  # データベースの全テーブルを作成
"""