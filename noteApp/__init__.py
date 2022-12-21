from flask import Flask
import os
import urllib
from flask_login import LoginManager, login_manager
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

db = SQLAlchemy()
KEY = "phuocDZ"
USERNAME = "dtdm-gg"
PASSWORD = "qwerty12"
DB_NAME = "todolist"


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = KEY
#    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://" + USERNAME +":"+ PASSWORD +"@/"+ DB_NAME + "?unix_socket=/cloudsql/absolute-advice-367518:us-central1:dtdm-note-app"
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:male0011@127.0.0.1:3306/testdb"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    
    from .models import Note, User
    with app.app_context():
        db.create_all()
    from .user import user
    from .views import views

    app.register_blueprint(user)
    app.register_blueprint(views)

    login_manager = LoginManager(app)
    login_manager.login_view = "user.login"
    login_manager.init_app(app)
    app.permanent_session_lifetime = timedelta(minutes=1)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
