'''
#flask : blueprint and views
@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response
'''

'''    
    customer_signin = LoginManager()
    customer_signin.login_view = 'auth.signin'
    customer_signin.init_app(app)

    @customer_signin.customer_loader
    def load_customer(customer_id):
        return Customer.query.get(int(customer_id))
    
    store_manager_signin = LoginManager()
    store_manager_signin.login_view = 'auth.signin'
    store_manager_signin.init_app(app)

    @store_manager_signin.store_manager_loader
    def load_store_manager(store_manager_id):
        return StoreManager.query.get(int(store_manager_id))
    
    delivery_executive_signin = LoginManager()
    delivery_executive_signin.login_view = 'auth.signin'
    delivery_executive_signin.init_app(app)

    @delivery_executive_signin.delivery_executive_loader
    def load_delivery_executive(delivery_executive_id):
        return DeliveryExecutive.query.get(int(delivery_executive_id))
    '''


'''
<!--
<!DOCTYPE html>
<html>
<head>
	<meta charset="UTF-8">
	<title>Product Search</title>
	<style>
		body {
			font-family: Arial, sans-serif;
			margin: 0;
			padding: 0;
		}

		h1 {
			margin-top: 20px;
			margin-bottom: 10px;
			text-align: center;
		}

		.search-bar {
			display: flex;
			flex-direction: row;
			align-items: center;
			margin-top: 20px;
			margin-bottom: 20px;
			padding: 10px;
			border: 1px solid #ddd;
		}

		.search-bar label {
			font-size: 20px;
			margin-right: 10px;
		}

		.search-bar input[type="text"] {
			flex-grow: 1;
			font-size: 20px;
			padding: 5px;
			border: none;
		}

		.search-bar button {
			font-size: 20px;
			padding: 5px 10px;
			background-color: #6def85;
			color: #fff;
			border: none;
			border-radius: 5px;
			cursor: pointer;
		}

		.product-item {
			display: flex;
			flex-direction: row;
			margin-bottom: 20px;
			padding: 10px;
			border: 1px solid #ddd;
		}

		.product-item img {
			width: 200px;
			height: 200px;
			margin-right: 20px;
		}

		.product-item-details {
			flex-grow: 1;
		}

		.product-item-name {
			font-size: 24px;
			margin: 0;
			padding: 0;
		}

		.product-item-farm {
			font-style: italic;
			margin-top: 5px;
			margin-bottom: 5px;
		}

		.product-item-price {
			font-size: 18px;
			margin: 0;
			padding: 0;
			display: inline-block;
			margin-right: 20px;
		}

		.add-to-cart-button {
			display: inline-block;
			font-size: 20px;
			background-color: #6def85;
			color: #fff;
			border: none;
			border-radius: 5px;
			padding: 5px 10px;
			text-decoration: none;
			cursor: pointer;
		}
	</style>
</head>
<body>
	<h1>Product Search</h1>

	<!Search Bar>
	<div class="search-bar">
		<label for="search">Search:</label>
		<input type="text" id="search" name="search">
		<button type="button">Search</button>
	</div>

	<!Product List> 
	<div class="product-list">
		<! Product Item 1 >
		<div class="product-item">
			<img src="https://atlantablackstar.com/wp-content/uploads/2013/10/tomato.jpg" alt="Product Image">
			<div class="product-item-details">
				<h2 class="product-item-name">Tomato</h2>
				<p class="product-item-farm">Garden Fresh Farm</p>
				<p class="product-item-price">Rs. 10</p>
				<button class="add-to-cart-button">Add to Cart</button>
			</div>
		</div>

        <! Product Item 2 >
		<div class="product-item">
			<img src="https://www.theayurveda.org/wp-content/uploads/2015/08/Ladyfinger-vegetable.png" alt="Product Image">
			<div class="product-item-details">
				<h2 class="product-item-name">Lady finger</h2>
				<p class="product-item-farm">Garden Fresh Farm</p>
				<p class="product-item-price">Rs. 20</p>
				<button class="add-to-cart-button">Add to Cart</button>
			</div>
		</div>

        </div>
        </body>
        </html>
	-->
'''


forgot password

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