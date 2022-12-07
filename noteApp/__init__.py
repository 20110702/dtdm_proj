from flask import Flask
import os
from flask_login import LoginManager, login_manager
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

db = SQLAlchemy()
KEY = "phuocDZ"
# DB_NAME = "mysql://root:Male0011@34.66.185.172/todolist"
DB_NAME = "mysql+pymysql://root:male0011@localhost/testdb"

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = DB_NAME
    db.init_app(app)
    
    from .models import Note, User
    with app.app_context():
        db.create_all()
    from .user import user
    from .views import views

    app.register_blueprint(user)
    app.register_blueprint(views)

    login_manager = LoginManager()
    login_manager.login_view = "user.login"
    login_manager.init_app(app)
    app.permanent_session_lifetime = timedelta(minutes=1)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
