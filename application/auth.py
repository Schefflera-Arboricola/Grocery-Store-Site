from flask import Blueprint, render_template, request, flash, redirect, url_for,session
from flask_login import login_user, login_required, logout_user, current_user
from flask import current_app as app
from application.models import *
from application.database import db

auth = Blueprint('auth', __name__)


@auth.route('/', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')          
        if role=='customer': user = Customer.query.filter_by(username=username).first()
        elif role=='store-manager': user = StoreManager.query.filter_by(username=username).first()
        elif role=='delivery-executive': user = DeliveryExecutive.query.filter_by(username=username).first()
        else: flash("Please select a role before proceeding to sign in.", category='error')
        if user:
            if user.password== password:
                login_user(user, remember=True)
                if role=='customer': 
                    session['account_type'] = 'Customer'
                    return render_template('dashboard/dashboard_customer.html', user=current_user)
                elif role=='store-manager': 
                    session['account_type'] = 'StoreManager'
                    return render_template('dashboard/dashboard_storemng.html', user=current_user)
                elif role=='delivery-executive': 
                    session['account_type'] = 'DeliveryExecutive'
                    return render_template('dashboard/dashboard_delexe.html', user=current_user)
                else: flash("Can't get the correct role. Report admin.", category='error')
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Username does not exist.', category='error')

    return render_template("signinup/signin_base.html")


@auth.route('/signout_customer')
@login_required
def logout_customer():
    logout_user()
    return redirect(url_for('auth.signin'))

@auth.route('/signout_store_manager')
@login_required
def logout_store_manager():
    logout_user()
    return redirect(url_for('auth.signin'))

@auth.route('/signout_delivery_executive')
@login_required
def logout_delivery_executive():
    logout_user()
    return redirect(url_for('auth.signin'))




@auth.route('/customer_signup', methods=['GET', 'POST'])
def customer_signup():
    if request.method == 'POST':  
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password') 
        phone = request.form.get('phone')
        email = request.form.get('email')
        address = request.form.get('address')

        user = Customer.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        else:
            new = Customer(email=email, name=name, password=password, username=username, phone_no=phone, address=address)
            db.session.add(new)
            db.session.commit()
            cart = Cart(customer_id=new.customer_id,product_id='NULL',quantity=0)
            db.session.add(cart)
            db.session.commit()
            login_user(new, remember=True)
            flash('Account created!', category='success')
            return redirect('/')
    return render_template('signinup/signup_customer.html')

@auth.route('/store_manager_signup', methods=['GET', 'POST'])
def store_manager_signup():
    if request.method == 'POST':  
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password') 
        phone = request.form.get('phone')
        email = request.form.get('email')

        user = StoreManager.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        else:
            new = StoreManager(email=email, name=name, password=password, username=username, phone_no=phone)
            db.session.add(new)
            db.session.commit()
            login_user(new, remember=True)
            flash('Account created!', category='success')
            return redirect('/')
    return render_template('signinup/signup_storemng.html')

@auth.route('/delivery_executive_signup', methods=['GET', 'POST'])
def delivery_executive_signup():
    if request.method == 'POST':  
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password') 
        phone = request.form.get('phone')
        email = request.form.get('email')
    
        user = DeliveryExecutive.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        else:
            new = DeliveryExecutive(email=email, name=name, password=password, username=username, phone_no=phone)
            db.session.add(new)
            db.session.commit()
            login_user(new, remember=True)
            flash('Account created!', category='success')
            return redirect('/')
    return render_template('signinup/signup_delexe.html')

