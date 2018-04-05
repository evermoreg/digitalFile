from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField, SubmitField
from flask_wtf.file import FileField
from wtforms.validators import InputRequired, Email, Length
from werkzeug.utils import secure_filename

class LoginForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

class messageForm(FlaskForm):
	pass
	#receiver=StringField('to', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
	#message=StringField('message')
	#file=FileField()
	#use this when combining JS and flask_form
	#sendMessage=SubmitField("Send", id="sendEncryptedMessage")

class profileForm(FlaskForm):
	phoneNumber = IntegerField('Phone Number')
	#password
	#publicKey
	#username

