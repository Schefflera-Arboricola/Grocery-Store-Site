'''
#flask : blueprint and views
@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response
'''

#<product search html page> : see on github


#forgot password

'''

#forgot password

# Route for handling forgot password request
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email') 
        role = request.form.get('role')  
        if role=='customer': user = Customer.query.filter_by(username=username).first()
        elif role=='store-manager': user = StoreManager.query.filter_by(username=username).first()
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
                'store-manager': StoreManager
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
alembic==0.9.10
Flask
Flask-Login==0.4.1
Flask-Migrate==2.2.1
Flask-SQLAlchemy==3.0.2
Flask-JWT==0.3.2
python-dateutil==2.7.3
python-editor==1.0.3
SQLAlchemy==1.4.44
requests==2.28.1
flask-swagger-ui==4.11.1
coverage==6.4
py-healthcheck==1.10.1
Flask-Testing==0.8.1
Jinja2==3.0.2
flask-restful
flask-cors
flask
'''