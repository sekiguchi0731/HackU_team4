from flask import render_template
from testapp import app

@app.route('/')
def index():
    data = "views.pyのinsert_something部分です。"
    return render_template("testapp/index.html",insert_something=data)

@app.route("/test")
def other1():
    return "テストページだよ"