from flask import Flask
import os
import urllib
from flask_login import LoginManager, login_manager
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

db = SQLAlchemy()
KEY = "phuocDZ"
# DB_NAME = "mysql://root:Male0011@34.66.185.172/todolist"
# DB_NAME = "mssql+pyodbc://NBP/testdb?driver=SQL Server?trusted_connection=yes,echo = True"

serverAddress = 'note-app-dtdm.mssql.somee.com'
usename='pnguyenba23_SQLLogin_1'
password='bwqvjjykvw'
databaseName='note-app-dtdm'
# params = urllib.parse.quote_plus('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+serverAddress+';DATABASE='+databaseName+';ENCRYPT=no;UID='+ usename +';PWD='+ password+ ';Trusted_Connection=yes;')
params = urllib.parse.quote_plus('DRIVER={ODBC Driver 17 for SQL Server};SERVER=note-app-dtdm.mssql.somee.com;packet size=4096;UID=pnguyenba23_SQLLogin_1;PWD=bwqvjjykvw;data source=note-app-dtdm.mssql.somee.com;persist security info=False;initial catalog=note-app-dtdm')
# params = urllib.parse.quote_plus('DRIVER={ODBC Driver 17 for SQL Server};SERVER=NBP;DATABASE=testdb;ENCRYPT=no;UID=nhoxphuoc;PWD=male0011;Trusted_Connection=yes;')

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = "mssql+pyodbc:///?odbc_connect=%s" % params
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
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
