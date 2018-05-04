from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_moment import Moment
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

app = Flask(__name__)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.config.from_object(Config)
app.config['BOOTSTRAP_SERVE_LOCAL']=True
app.config.from_pyfile('config.cfg')
bootstrap = Bootstrap(app)
moment=Moment(app)
mail=Mail(app)
s=URLSafeTimedSerializer(app.config['SECRET_KEY'])

'''migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
'''
from views import *

if __name__ == '__main__':
    app.run()