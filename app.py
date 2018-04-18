from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_moment import Moment

app = Flask(__name__)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.config.from_object(Config)
app.config['BOOTSTRAP_SERVE_LOCAL']=True
bootstrap = Bootstrap(app)
moment=Moment(app)

'''migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
'''
from views import *

if __name__ == '__main__':
    app.run()