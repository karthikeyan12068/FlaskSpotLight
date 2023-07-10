from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

# Security Key

app.config['SECRET_KEY']='9c8f7cfb7c60b59db0b81d7175797aa6'

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'

db=SQLAlchemy(app)

bcrypt=Bcrypt(app)

login_manager=LoginManager(app)

from webapp import routes