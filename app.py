from flask import Flask
from flask_bootstrap import Bootstrap
#from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
#from models import User

app = Flask(__name__)
app.config.from_pyfile('config.py')
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#@login_manager.user_loader
#def load_user(user_id):
#    return User.query.get(int(user_id))

from views import *

if __name__ == '__main__':
    app.run()