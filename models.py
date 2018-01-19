from app import app, db
from flask_login import UserMixin

class User(UserMixin, db.Model):
 #id = db.Column(db.Integer, primary_key=True)
    #username = db.Column(db.String(15), unique=True)
    email=db.Column(db.String(50), primary_key=True)
    password=db.Column(db.String(80))
    publicKey=db.Column(db.String(500))
    phoneNumber=db.Column(db.String(50))

    def get_id(self):
    	return str(self.email)

    def __repr__(self):
    	return '<User {}>'.format(self.email)
