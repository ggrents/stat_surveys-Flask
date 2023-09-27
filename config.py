from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate



app = Flask(__name__)

app.config['SECRET_KEY'] = "clsvDSFlvmdlks492dfksnK"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:2996@localhost/flask_app'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
migrate = Migrate(app, db)