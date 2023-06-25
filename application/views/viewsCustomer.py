from flask import Blueprint, render_template, request, flash, redirect, url_for,session
from flask_login import login_user, login_required, logout_user, current_user
from flask import current_app as app
from application.models import *
from application.database import db
from werkzeug.security import check_password_hash
from application.views.auth import check_address

viewsCustomer = Blueprint('viewsCustomer', __name__)

# Apply the login_required decorator to all routes in the viewsCustomer blueprint
@viewsCustomer.before_request
@login_required
def require_login():
    pass

@viewsCustomer.route('/customer/<int:c_id>/dashboard')
def dashboard(c_id):
    user=Customer.query.filter_by(customer_id=c_id).first()
    return render_template("dashboard/dashboard_customer.html", account_type='customer',id=c_id,name=user.name,address=user.address,phone=user.phone_no,username=user.username,email=user.email)

@viewsCustomer.route('/customer/<int:c_id>/editProfile', methods=['GET', 'POST'])
def editProfile(c_id):
    if request.method == 'POST':
        name=request.form.get('name')
        phone=request.form.get('phone')
        address=request.form.get('address')
        password=request.form.get('password')
        user=Customer.query.filter_by(customer_id=c_id).first()
        user.name=name
        user.phone_no=phone
        user.address=address
        if check_password_hash(user.password, password):
            features=check_user_features(name,phone)
            add=check_address(address)
            if features!=True: 
                flash(features, category='error')
                return render_template("editProfile/editProfile_customer.html", name=user.name,phone=user.phone_no,address=user.address)
            elif add!=True: 
                flash(add, category='error')
                
            else:
                db.session.commit()
                return redirect(url_for('viewsCustomer.dashboard',c_id=c_id))
        else:
            flash('Incorrect password, try again.', category='error')
            return render_template("editProfile/editProfile_customer.html",name=user.name,address=user.address,phone=user.phone_no)
    else:
        user=Customer.query.filter_by(customer_id=c_id).first()
        return render_template("editProfile/editProfile_customer.html", name=user.name,address=user.address,phone=user.phone_no)

def check_user_features(name,phone):
    if len(phone)!=10 and phone.isdigit():
        return 'Phone number must have 10 digits'
    elif type(name)!=str:
        return 'Name must be a string'
    else: return True
      
@viewsCustomer.route('/customer/<int:c_id>/cart')
def cart(c_id):
    return render_template("userviews/customer/goToCart.html", cid=c_id)

@viewsCustomer.route('/customer/<int:c_id>/past_orders')
def past_orders(c_id):
    return render_template("userviews/customer/pastOrders.html", cid=c_id)

@viewsCustomer.route('/customer/searchProducts', methods=['GET', 'POST'])
def searchProducts():
    return render_template("userviews/customer/searchProducts.html")

