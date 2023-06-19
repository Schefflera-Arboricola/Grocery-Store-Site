from flask import Blueprint, render_template, request, flash, redirect, url_for,session
from flask_login import login_user, login_required, logout_user, current_user, LoginManager
from flask import current_app as app
from application.models import *
from application.database import db

def LoginManagerfunc(app):
    login_manager = LoginManager()
    login_manager.login_view = 'auth.signin'
    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(user_id):
        # Determine the user type based on the prefix in the user_id
        if session['account_type'] == 'Customer':
            return Customer.query.get(int(user_id))
        elif session['account_type'] == 'StoreManager':
            return StoreManager.query.get(int(user_id))
        elif session['account_type'] == 'DeliveryExecutive':
            return DeliveryExecutive.query.get(int(user_id))
        else:
            return None
            
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

        validate_features=check_user_features(Customer,name,username,phone,password,email)
        validate_address=check_address(address)
        if validate_features!=True: flash(validate_features, category='error')
        elif validate_address!=True: flash(validate_address, category='error')
        else:
            new = Customer(email=email, name=name, password=password, username=username, phone_no=phone, address=address)
            db.session.add(new)
            db.session.commit()
            cart = Cart(customer_id=new.customer_id,product_id='NULL',quantity=0)
            db.session.add(cart)
            db.session.commit()
            flash('Account created!', category='success')
            #feature : send email('thanks for signing up! verify your email : <link>')
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
        strmng_id = request.form.get('store-manager-id')
        branch_id = request.form.get('branch-id')
        
        validate_features=check_user_features(StoreManager,name,username,phone,password,email)
        validate_strmng_ids=check_strmng_ids(int(strmng_id),int(branch_id))
        if validate_features!=True: flash(validate_features, category='error')
        elif validate_strmng_ids!=True: flash(validate_strmng_ids, category='error')
        else:
            new = StoreManager(store_manager_id=int(strmng_id),branch_id=int(branch_id),email=email, name=name, password=password, username=username, phone_no=phone)
            db.session.add(new)
            db.session.commit()
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
        delexe_id = request.form.get('delivery-executive-id')
        branch_id = request.form.get('branch-id')

        validate_features=check_user_features(DeliveryExecutive,name,username,phone,password,email)
        validate_delexe_ids=check_delexe_ids(int(delexe_id),int(branch_id))
        if validate_features!=True: flash(validate_features, category='error')
        elif validate_delexe_ids!=True: flash(validate_delexe_ids, category='error')
        else:
            new = DeliveryExecutive(delivery_executive_id=int(delexe_id),branch_id=int(branch_id),email=email, name=name, password=password, username=username, phone_no=phone)
            db.session.add(new)
            db.session.commit()
            flash('Account created!', category='success')
            return redirect('/')
    return render_template('signinup/signup_delexe.html')


def check_user_features(dbClass,name,username,phone,password,email):
    if dbClass.query.filter_by(username=username).first():
        return 'Username already exists'    
    elif len(username)<8 : 
        return 'Username must have atleast 8 characters'
    elif dbClass.query.filter_by(email=email).first():
        return 'Email already exists'
    elif type(email)!=str:
        return 'Email must be a string'
    elif len(password)<8 :
        return 'Password must have atleast 8 characters'
    elif len(phone)!=10 and phone.isdigit():
        return 'Phone number must have 10 digits'
    elif type(name)!=str:
        return 'Name must be a string'
    else:
        return True

def check_address(address):
    if type(address)!=str:
        return 'Address must be a string'
    elif len(address)<10:
        return 'Address must have atleast 10 characters'
    else:
        return True
    
def check_strmng_ids(strmng_id, branch_id):
    strmng_entry = StoreManagerids.query.filter_by(store_manager_id=strmng_id, branch_id=branch_id).first()
    if strmng_entry:
        return True
    elif not StoreManagerids.query.filter_by(store_manager_id=strmng_id).first():
        return 'Enter correct Store Manager ID'
    elif not StoreManagerids.query.filter_by(branch_id=branch_id).first():
        return 'Enter correct Branch ID'
    else:
        return 'Something went wrong! Contact Admin.'


def check_delexe_ids(delexe_id,branch_id):
    delexe_entry = DeliveryExecutiveids.query.filter_by(delivery_executive_id=delexe_id, branch_id=branch_id).first()
    if delexe_entry:
        return True
    elif not DeliveryExecutiveids.query.filter_by(delivery_executive_id=delexe_id).first():
        return 'Enter correct Delivery Executive ID'
    elif not DeliveryExecutiveids.query.filter_by(branch_id=branch_id).first():
        return 'Enter correct Branch ID'
    else:
        return 'Something went wrong! Contact Admin.'
