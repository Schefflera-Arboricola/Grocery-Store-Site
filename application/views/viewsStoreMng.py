from flask import Blueprint, render_template, request, flash, redirect, url_for,session
from flask_login import login_user, login_required, logout_user, current_user, LoginManager
from flask import current_app as app
from application.models import *
from application.database import db
from werkzeug.security import check_password_hash

viewsStoreMng = Blueprint('viewsStoreMng', __name__)

@viewsStoreMng.before_request
@login_required
def require_login():
    pass

@viewsStoreMng.route('/storemng/<int:strmng_id>/dashboard')
def dashboard(strmng_id):
    user=StoreManager.query.filter_by(store_manager_id=strmng_id).first()
    return render_template("dashboard/dashboard_storemng.html",id=strmng_id,name=user.name,phone=user.phone_no,username=user.username,email=user.email,account_type='storemng')

@viewsStoreMng.route('/storemng/<int:strmng_id>/editProfile', methods=['GET', 'POST'])
def editProfile(strmng_id):
    if request.method == 'POST':
        name=request.form.get('name')
        phone=request.form.get('phone')
        password=request.form.get('password')
        user=StoreManager.query.filter_by(store_manager_id=strmng_id).first()
        user.name=name
        user.phone_no=phone
        if check_password_hash(user.password, password):
            features=check_user_features(StoreManager,name,user.username,phone,password,user.email)
            if features!=True: 
                flash(features, category='error')
                return render_template("editProfile/editProfile_storemng.html", name=user.name,phone=user.phone_no)
            else:
                db.session.commit()
                return redirect(url_for('viewsStoreMng.dashboard',strmng_id=strmng_id))
        else:
            flash('Incorrect password, try again.', category='error')
            return render_template("editProfile/editProfile_storemng.html", name=user.name,phone=user.phone_no)
    else:
        user=StoreManager.query.filter_by(store_manager_id=strmng_id).first()
        return render_template("editProfile/editProfile_storemng.html",name=user.name,phone=user.phone_no)
    
def check_user_features(name,phone):
    if len(phone)!=10 and phone.isdigit():
        return 'Phone number must have 10 digits'
    elif type(name)!=str:
        return 'Name must be a string'
    else: return True
    
@viewsStoreMng.route('/storemng/Products', methods=['GET', 'POST'])
def Products():
    return render_template("userviews/store_manager/viewProducts.html")

@viewsStoreMng.route('/storemng/Category', methods=['GET', 'POST'])
def Category():
    return render_template("userviews/store_manager/viewCategories.html")