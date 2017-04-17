from flask import Flask
from flask_login import LoginManager
from flask_wtf import CsrfProtect
from flask_sqlalchemy import SQLAlchemy
from app.ErrorHandler import errors
app = Flask(__name__)
app.config.from_object('flask_config')
db = SQLAlchemy(app)
CsrfProtect(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.register_blueprint(errors)

from app import views, models
