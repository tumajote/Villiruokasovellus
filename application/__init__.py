from flask_login import LoginManager
from os import urandom
from application.auth.models import User
from application.auth import views
from application.auth import models
from application.saalis import views
from application.saalis import models
from application import views
import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)


if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///saalis.db"
    app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)


# kirjautuminen
app.config["SECRET_KEY"] = urandom(32)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth_login"
login_manager.login_message = "Please login to use this functionality."


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


try:
    db.create_all()
except:
    pass
