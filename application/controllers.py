'''
#flask : blueprint and views
@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response
'''

#from werkzeug.security import generate_password_hash, check_password_hash
#from flask_login import login_user, login_required, logout_user, current_user

#main = Blueprint('main', __name__)

from flask import Flask, redirect, url_for, flash, render_template, request, Blueprint
from flask import current_app as app
from application.models import *
from application.database import db
from datetime import datetime, timedelta
import random
import string

@app.route('/', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':  
        username = request.form.get('username')
        password = request.form.get('password') 
        role = request.form.get('role')          
        if role=='customer': user = Customer.query.filter_by(username=username).first()
        elif role=='store-manager': user = StoreManager.query.filter_by(username=username).first()
        elif role=='app-manager': user = AppManager.query.filter_by(username=username).first()
        else: flash("Please select a role before proceeding to sign in.", category='error')
        if user:
            if (user.password==password):
                temp='dashboard/'+role+'_dashboard.html'
                return render_template(temp)
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('User does not exist.', category='error')
    return render_template('signinup/base_signin.html')


@app.route('/customer_signup', methods=['GET', 'POST'])
def customer_signup():
    if request.method == 'POST':  
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password') 
        phone = request.form.get('phone')

    return render_template('signinup/customer_signup.html')

@app.route('/store_manager_signup', methods=['GET', 'POST'])
def store_manager_signup():
    return render_template('signinup/storemng_signup.html')

@app.route('/app_manager_signup', methods=['GET', 'POST'])
def app_manager_signup():
    return render_template('signinup/appmng_signup.html')

#forgot password
'''
# Route for handling forgot password request
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email') 
        role = request.form.get('role')  
        role_mapping = {
                'customer': Customer,
                'store-manager': StoreManager,
                'app-manager': AppManager
            }
        if role in role_mapping:
            user = role_mapping[role].query.filter_by(username=username).filter_by(email=email).first()
        else: flash("Please select a role before proceeding to sign in.", category='error')
        if user:
            # Generate a secure token for password reset
            token = generate_token()

            # Store the token, email, and expiration time in a database or cache
            store_token(token, email)

            # Send the password reset email with the token embedded
            send_password_reset_email(email, token)

            flash('A password reset email has been sent to your email address.')
            return redirect(url_for('signin'))
        else:
            flash('Email address not found in our records.')
    
    return render_template('forgot_password.html')


# Route for handling password reset with token
@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token,role):
    # Verify the token against the stored token in the database or cache
    email = verify_token(token)
    role_mapping = {
                'customer': Customer,
                'store-manager': StoreManager,
                'app-manager': AppManager
            }
    if not email:
        flash('Invalid or expired password reset link.')
        return redirect(url_for('signin'))
    
    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password == confirm_password:
            # Update the user's password in the database
            user = role_mapping[role].query.filter_by(email=email).first()
            user.password = password
            db.session.commit()
            flash('Your password has been reset successfully. Please sign in with your new password.')
            return redirect(url_for('signin'))
        else:
            flash('Passwords do not match.')
    
    return render_template('reset_password.html', token=token)


def generate_token():
    # Generate a random alphanumeric token
    characters = string.ascii_letters + string.digits
    token = ''.join(random.choice(characters) for _ in range(20))
    return token


def store_token(token, email):
    # Store the token, email, and expiration time in a database or cache
    # Example: save the token, email, and expiration time in the PasswordReset model
    expiration_time = datetime.now() + timedelta(hours=1)
    password_reset = PasswordReset(token=token, email=email, expiration_time=expiration_time)
    db.session.add(password_reset)
    db.session.commit()


def verify_token(token):
    # Verify the token against the stored token in the database or cache
    # Example: retrieve the email associated with the token from the PasswordReset model
    password_reset = PasswordReset.query.filter_by(token=token).first()
    if password_reset and password_reset.expiration_time > datetime.now():
        return password_reset.email
    return None

from flask_mail import Message
from application import mail

def send_password_reset_email(email, token):
    # Send the password reset email to the user
    # You can use a library or email service of your choice to send the email
    # Example using Flask-Mail:
    # mail.send_message(
    #     subject='Password Reset',
    #     recipients=[email],
    #     body=f"Click the following link to reset your password: {url_for('reset_password', token=token, _external=True)}"
    # )

    # Replace the above code with your chosen email service implementation
    password_reset_url = url_for('reset_password', token=token, _external=True)
    
    message = Message(
        subject='Password Reset',
        recipients=[email],
        body=f"Click the following link to reset your password: {password_reset_url}"
    )
    mail.send(message)
    return None

    '''


'''
@app.route('/ulogin', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = Customer.query.filter_by(cemail=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@app.route('/ulogout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@app.route('/usign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        cname = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = Customer.query.filter_by(cemail=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(cname) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = Customer(cemail=email, cname=cname, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("customer_signup.html", user=current_user)

'''