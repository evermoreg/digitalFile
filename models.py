from app import app, db
from flask_login import UserMixin
from datetime import datetime
from io import BytesIO
import os

class User(UserMixin, db.Model):
    email=db.Column(db.String(50), primary_key=True)
    password=db.Column(db.String(80))
    #publicKey=db.Column(db.String(500))
    #phoneNumber=db.Column(db.String(50))
    messageSent=db.relationship('Messages', backref='author', lazy='dynamic')

    def get_id(self):
    	return str(self.email)

    def __repr__(self):
    	return '<User {}>'.format(self.email)

class Messages(db.Model):
	id=db.Column(db.Integer, primary_key=True)
	receiver=db.Column(db.String(50))
	file=db.Column(db.LargeBinary)
	message=db.Column(db.String(500))
	timestamp=db.Column(db.DateTime, index=True, default=datetime.utcnow)
	sender=db.Column(db.String(50), db.ForeignKey('user.email'))

	def __repr__(self):
		return '<Message {} {}>'.format(self.message, self.file)

