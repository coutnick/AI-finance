from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finaince.db'
app.config['SECRET_KEY'] = '3DBB2ED6E9EDD9F15B82782A58B86'
app.config['JWT_SECRET_KEY'] = 'e55b8def7445397f6b45b4e9ad475cf5b6549132e58e5816f0efa05c2e90b090917f537fdc68f997365bb7e197c7ecc0f55bbd84f9ebcea9c3473a997d8576cde10af4d9ec87366b526bdccbfedd876de897dffd874e3871be9f3ae69957deead25cef75e9459d5765e9590aa9c77714aac7d5e647fe4b3aa3deb0f247424eee63d08791d769453d8f9ac1b5012b7ce957e141e7e5b920886d86b9f24e68d068029be7be0cda5c3741925dd34a59519d722fe591f378a63ed3e8e513b139593e6617cca064e3d2f97bff1fc690143cc7f84bcf1e0406a1a6daff72104cf6513f4bf687054ef6fa9472bee2a50fa04fefabb81b067fbdfc8ad994771bcfa45725'

db = SQLAlchemy(app)
migrage = Migrate(app, db)
jwt = JWTManager(app)

# Import models after db is created 
from models import User

if __name__ == '__main__':
    app.run(debug=True)