from datetime import timedelta

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging.config import dictConfig
import logging

custom_logger = logging.getLogger('app')
custom_logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('my_info.log')
console_handler = logging.StreamHandler()

console_handler.setLevel(logging.ERROR)


formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

custom_logger.addHandler(file_handler)
custom_logger.addHandler(console_handler)

app = Flask(__name__)

app.config['SECRET_KEY'] = "clsvDSFlvmdlks492dfksnK"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:2996@localhost/flask_app'

app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
migrate = Migrate(app, db)
