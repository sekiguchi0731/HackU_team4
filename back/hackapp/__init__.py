from flask import Flask 
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object("hackapp.config")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop_system.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
from .models import restaurants

import hackapp.views