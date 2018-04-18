from app import app, login_manager, db
from flask import redirect, url_for, request, send_file
from forms import LoginForm, RegisterForm, messageForm, profileForm
from flask import render_template
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from models import User, Messages
from sqlalchemy import desc
from io import BytesIO
from smsAPI import Twilio

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('home'))
        return '<h1>Invalid username or password</h1>'    
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        email=form.email.data
        # TODO: Issue 1 -- validate users email. email has a unique constraint in the database.
        #print(User.query.filter_by(email=email).all())
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return '<h1>New user has been created!</h1>'
    return render_template('signup.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.email)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def home():
    contactList=User.query.all()
    return render_template('home.html', contactList=contactList, name=current_user.email)

@app.route('/upload', methods=['POST'])
@login_required
def upload():
    form=messageForm()
    if not form.validate_on_submit():
     
        receiver=request.form['recipientName']
        #recipient line mistakenly deleted
        aesEncryptedMessage=request.form['encryptedMessage']
        rsaEncryptedKey=request.form['rsaEncryptedKey']

        ''' #message=form.message.data
        #files are temporarily disabled
        file=form.file.data
        filename=secure_filename(file.filename)
        '''
        #add security checks

        #newMessage = Messages(sender=current_user.email, receiver=receiver, file=file.read(), message=message)
        newMessage = Messages(sender=current_user.email, receiver=receiver, message=aesEncryptedMessage, rsaEncryptedKey=rsaEncryptedKey)
        db.session.add(newMessage)
        db.session.commit()

        '''receiverPhone=User.query.filter_by(email=receiver).first()
        phoneNumber="+263"+str(receiverPhone.phoneNumber)
        Twilio.phoneMessage(phoneNumber, current_user.email)
        '''
        return 'Saved ' + ' to the database! from user ' + current_user.email
    return "Not sent"

@app.route('/inbox')
@login_required
def inbox():
    messages=Messages.query.filter_by(receiver=current_user.email).all()
    return render_template('inbox.html', messages=messages, name=current_user.email)

@app.route('/readMessage/<senderID>')
@login_required
def readMessage(senderID):
    message=Messages.query.get(senderID)
    return render_template('readMessage.html', message=message)
    
@app.route('/download/<fileID>')
@login_required
def download(fileID):
    messages=Messages.query.get(fileID)
    return send_file(BytesIO(messages.file), attachment_filename='test1.pdf', as_attachment=True)

@app.route('/compose')    
@login_required
def compose():
    #form=messageForm()
    #receiver=contactID
    return render_template('compose.html') #, form=form

@app.route('/profile', methods=['POST', 'GET'])
@login_required
def profile():
    form=profileForm()
    if form.validate_on_submit():
        #TODO: update the database
        current_user.phoneNumber=form.phoneNumber.data
        #add users public key to to databse
        current_user.publicKey=form.publicKey.data
        print(current_user.publicKey)
        current_user.signingKey=request.form.get('hideSigningKey')
        db.session.commit()
        #flash('Your changes have been saved.')
        return redirect(url_for('profile'))
    elif request.method =='GET':
        form.phoneNumber.data=current_user.phoneNumber
    return render_template('profile.html', form=form)

@app.route('/test1', methods=['POST', 'GET'])
def test1():

    encryptedText=request.form.get("encryptedText")
    encryptionKey=request.form.get("encryptionKey")
    return "Your encrypted message is:" +  encryptedText + " the encryption key is: " + encryptionKey

@app.route('/checkEmail', methods=['POST', 'GET'])
@login_required
def checkEmail():
    if request.method=='POST':
        #validation
        recipientEmail=request.form['recipientEmail']
        recipient=User.query.filter_by(email=recipientEmail).first()
        
        return render_template('compose.html', recipient=recipient)
    else:
        return render_template('checkEmail.html')
    

