import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///achievements.db'
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['APPMAP'] = True
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message = "Ta strona jest zabezpieczina. Aby wejść na tą stronę musisz się najpierw zalogować."
login_manager.login_message_category = "info"

from market import routes
