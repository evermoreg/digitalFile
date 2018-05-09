from app import app, login_manager, db, s, mail, SignatureExpired
from flask import redirect, url_for, request, send_file, render_template
from forms import LoginForm, RegisterForm, messageForm, profileForm
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from models import User, Messages
from sqlalchemy import desc
from io import BytesIO
from smsAPI import Twilio
from flask_mail import Mail, Message



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
        if User.query.filter_by(email=form.email.data).first() != None:
            return '<h1>Invalid login details exists</h1>'
        else:
            #sending confirmation mail to user

            token=s.dumps(email, salt='email-confirm')

            msg=Message('Confirm email', sender='tatalmondmush@gmail.com', recipients=[email])
            link=url_for('confirmMail', token=token, _external=True)
            msg.body='Click the link: {} to confirm your email'.format(link)
            mail.send(msg)


            #adding user to database
            hashed_password = generate_password_hash(form.password.data, method='sha256')
            new_user = User(email=form.email.data, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()

            return '<h1>New user has been created!</h1>'
    return render_template('signup.html', form=form)

@app.route('/confirmMail/<token>')
def confirmMail(token):
    try:
        email=s.loads(token, salt='email-confirm', max_age=3600)
        user=User.query.filter_by(email=email).first()
        user.confirmMail='True'
        db.session.commit()
    except SignatureExpired:
        return 'signature expired'
    return 'token works'  
    

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

        #message=form.message.data
        #files are temporarily disabled
        print("working")
        file=request.files['encryptedFile']
        filename=secure_filename(file.filename)
        #add security checks
        print("working ffffine")
        #newMessage = Messages(sender=current_user.email, receiver=receiver, file=file.read(), message=message)
        newMessage = Messages(sender=current_user.email, receiver=receiver, message=aesEncryptedMessage, rsaEncryptedKey=rsaEncryptedKey, file=file.read(), filename=filename)
        db.session.add(newMessage)
        db.session.commit()
        
        #sending a notification text nested in try; except because of weak internet connections
        #surround with try; catch
        receiverPhone=User.query.filter_by(email=receiver).first()
        phoneNumber="+263"+str(receiverPhone.phoneNumber)
        print(phoneNumber)
        '''
        Twilio.phoneMessage(phoneNumber, current_user.email)
        '''
        
        return render_template('messageSent.html', current_user=current_user.email, receivePhone=phoneNumber, receive=receiver)
        #return 'Message has been sent from user ' + current_user.email
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
    return send_file(BytesIO(messages.file), attachment_filename=messages.filename, as_attachment=True)

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
        allKeys=User.query.filter_by().all()
        return render_template('checkEmail.html', allKeys=allKeys)
    

