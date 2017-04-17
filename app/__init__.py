from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import CsrfProtect

app = Flask(__name__)
app.config.from_object('flask_config')
db = SQLAlchemy(app)
#app.secret_key = 'MY_KEY_IS_STRONG'
#CsrfProtect(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from app import views, models
