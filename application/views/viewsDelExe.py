from flask import Blueprint, render_template, request, flash, redirect, url_for,session
from flask_login import login_user, login_required, logout_user, current_user, LoginManager
from flask import current_app as app
from application.models import *
from application.database import db
from werkzeug.security import check_password_hash
import requests

viewsDelExe = Blueprint('viewsDelExe', __name__)

@viewsDelExe.before_request
@login_required
def require_login():
    pass

@viewsDelExe.route('/delexe/<int:delexe_id>/dashboard')
def dashboard(delexe_id):
    user=DeliveryExecutive.query.filter_by(delivery_executive_id=delexe_id).first()
    return render_template("dashboard/dashboard_delexe.html",id=delexe_id,name=user.name,phone=user.phone_no,username=user.username,email=user.email,account_type='delexe')

@viewsDelExe.route('/delexe/<int:delexe_id>/editProfile', methods=['GET', 'POST'])
def editProfile(delexe_id):
    if request.method == 'POST':
        name=request.form.get('name')
        phone=request.form.get('phone')
        password=request.form.get('password')
        user=DeliveryExecutive.query.filter_by(delivery_executive_id=delexe_id).first()
        user.name=name
        user.phone_no=phone
        if check_password_hash(user.password, password):
            features=check_user_features(DeliveryExecutive,name,user.username,phone,password,user.email)
            if features!=True: 
                flash(features, category='error')
                return render_template("editProfile/editProfile_delexe.html", name=user.name,phone=user.phone_no)
            else:
                db.session.commit()
                return redirect(url_for('viewsDelExe.dashboard',delexe_id=delexe_id))
        else:
            flash('Incorrect password, try again.', category='error')
            return render_template("editProfile/editProfile_delexe.html", id=delexe_id,name=user.name,phone=user.phone_no,username=user.username,email=user.email)
    else:
        user=DeliveryExecutive.query.filter_by(delivery_executive_id=delexe_id).first()
        return render_template("editProfile/editProfile_delexe.html", id=delexe_id,name=user.name,phone=user.phone_no,username=user.username,email=user.email)
    
def check_user_features(name,phone):
    if len(phone)!=10 and phone.isdigit():
        return 'Phone number must have 10 digits'
    elif type(name)!=str:
        return 'Name must be a string'
    else: return True

@viewsDelExe.route('/delexe/<int:delexe_id>/pendingDelieveries', methods=['GET', 'POST'])
def pendingDelieveries(delexe_id):
    orders=OrderDetails.query.filter_by(delivery_executive_id=delexe_id,delivery_status='ORDER PLACED').all()
    return render_template("userviews/delivery_executive/pending_deliveries.html",delexe_id=delexe_id,orders=orders)

@viewsDelExe.route('/delexe/<int:delexe_id>/completedDelieveries', methods=['GET', 'POST'])
def completedDelieveries(delexe_id):
    orders=OrderDetails.query.filter_by(delivery_executive_id=delexe_id,delivery_status='DELIVERED').all()
    return render_template("userviews/delivery_executive/completed_deliveries.html",delexe_id=delexe_id,orders=orders)

@viewsDelExe.route('/delexe/<int:delexe_id>/delivery_details/<int:order_id>', methods=['GET', 'POST'])
def delivery_details(delexe_id,order_id):
    order=OrderDetails.query.filter_by(order_id=order_id).first()
    customer=Customer.query.filter_by(customer_id=order.customer_id).first()
    customer={'name': customer.name ,'phone' : customer.phone_no,'address': customer.address}
    orderItems=OrdersItems.query.filter_by(order_id=order_id).all()
    products=[]
    for i in orderItems:
        d={'quantity': i.quantity,'price': i.price}
        name=Products.query.filter_by(product_id=i.product_id).first().name #use api instead
        d['name']=name
        products.append(d)
    total_price=order.total_price
    if request.method == 'POST':
        order.delivery_status='DELIVERED'
        db.session.commit()
    return render_template("userviews/delivery_executive/delivery_details.html",delexe_id=delexe_id,order_id=order_id,customer=customer,products=products,total_price=total_price,delivery_status=order.delivery_status)
        