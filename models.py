from app import db, app
from flask_login import UserMixin
'''from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
'''
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email=db.Column(db.String(50))
    password=db.Column(db.String(80))
    #publicKey=db.Column(db.String(500))
    #phoneNumber=db.Column(db.String(50))

    '''def __repr__(self):
    	return '<User {}>'.format(self.email)

if __name__ == '__main__':
	manager.run()
'''