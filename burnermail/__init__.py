from pathlib import Path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
# Set secret key -- turn into env var
app.config['SECRET_KEY'] = 'cfdfb214f97bb74e2f6d51bc2ec404ea'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

all_words = set(x.strip() for x in open('burnermail/static/language/words_alpha.txt') if len(x) < 7)
bad_words = set(x.strip() for x in open('burnermail/static/language/bad_words.txt'))
usable_words = all_words - bad_words

from burnermail import routes
