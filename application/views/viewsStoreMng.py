from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from flask import current_app as app
from application.models import *
from application.database import db
from werkzeug.security import check_password_hash
import requests

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
            features=check_user_features(name,phone)
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
    


# Product Management

@viewsStoreMng.route('/storemng/<int:strmng_id>/Product', methods=['GET', 'POST'])
def Product(strmng_id):
    base_url = request.host_url[:-1]
    response = requests.get(f'{base_url}/products')
    products=response.json()
    return render_template("userviews/store_manager/viewProducts.html",products=products, strmng_id=strmng_id)

@viewsStoreMng.route('/storemng/<int:strmng_id>/addProduct', methods=['GET', 'POST'])
def addProduct(strmng_id):
    if request.method=='POST':
        base_url = request.host_url[:-1]
        response = requests.post(f'{base_url}/products', json=request.form)
        products=response.json()
        if response.status_code==404:
            flash(products['message'], category='error')
        elif response.status_code==201:
            return redirect(url_for('viewsStoreMng.Product',strmng_id=strmng_id))
        else:
            flash('Something went wrong. Contact Admin', category='error')
    return render_template("userviews/store_manager/addProduct.html")

@viewsStoreMng.route('/storemng/<int:strmng_id>/editProduct/<int:prod_id>', methods=['GET', 'POST'])
def editProduct(strmng_id,prod_id):
    if request.method=='POST':
        base_url = request.host_url[:-1]
        response = requests.put(f'{base_url}/products/{prod_id}', json=request.form)
        products=response.json()
        if response.status_code==404:
            flash(products['message'], category='error')
        elif response.status_code==201:
            return redirect(url_for('viewsStoreMng.Product',strmng_id=strmng_id))
        else:
            flash('Something went wrong. Contact Admin', category='error')
    product=Products.query.filter_by(product_id=prod_id).first()
    return render_template("userviews/store_manager/editProduct.html", product=product)

@viewsStoreMng.route('/storemng/<int:strmng_id>/deleteProduct/<int:prod_id>', methods=['GET', 'POST'])
def deleteProduct(strmng_id,prod_id):
    base_url = request.host_url[:-1]
    response = requests.delete(f'{base_url}/products/{prod_id}')
    products=response.json()
    if response.status_code==404:
        print(products['message'])
    elif response.status_code==201:
        return redirect(url_for('viewsStoreMng.Product',strmng_id=strmng_id))
    else:
        print('Something went wrong. Contact Admin')
    return redirect(url_for('viewsStoreMng.Product',strmng_id=strmng_id))




# Category Management

@viewsStoreMng.route('/storemng/<int:strmng_id>/Category', methods=['GET', 'POST'])
def Categories(strmng_id):
    base_url = request.host_url[:-1]
    response = requests.get(f'{base_url}/categories')
    categories=response.json()
    return render_template("userviews/store_manager/viewCategories.html",categories=categories, strmng_id=strmng_id)

@viewsStoreMng.route('/storemng/<int:strmng_id>/addCategory', methods=['GET', 'POST'])
def addCategory(strmng_id):
    if request.method=='POST':
        base_url = request.host_url[:-1]
        response = requests.post(f'{base_url}/categories', json=request.form)
        categories=response.json()
        if response.status_code==404:
            flash(categories['message'], category='error')
        elif response.status_code==201:
            return redirect(url_for('viewsStoreMng.Categories',strmng_id=strmng_id))
        else:
            flash('Something went wrong. Contact Admin', category='error')
    return render_template("userviews/store_manager/addCategory.html")

@viewsStoreMng.route('/storemng/<int:strmng_id>/editCategory/<int:cat_id>', methods=['GET', 'POST'])
def editCategory(strmng_id,cat_id):
    category=Category.query.filter_by(category_id=cat_id).first()
    if request.method=='POST':
        base_url = request.host_url[:-1]
        response = requests.put(f'{base_url}/categories/{cat_id}', json=request.form)
        categories=response.json()
        if response.status_code==404:
            flash(categories['message'], category='error')
        elif response.status_code==201:
            return redirect(url_for('viewsStoreMng.Categories',strmng_id=strmng_id))
        else:
            flash('Something went wrong. Contact Admin', category='error')
    return render_template("userviews/store_manager/editCategory.html", category=category)

@viewsStoreMng.route('/storemng/<int:strmng_id>/deleteCategory/<int:cat_id>', methods=['GET', 'POST'])
def deleteCategory(strmng_id,cat_id):
    base_url = request.host_url[:-1]
    response = requests.delete(f'{base_url}/categories/{cat_id}')
    categories=response.json()
    if response.status_code==404:
        print(categories['message'])
    elif response.status_code==201:
        return redirect(url_for('viewsStoreMng.Categories',strmng_id=strmng_id))
    else:
        print('Something went wrong. Contact Admin')
    return redirect(url_for('viewsStoreMng.Categories',strmng_id=strmng_id))