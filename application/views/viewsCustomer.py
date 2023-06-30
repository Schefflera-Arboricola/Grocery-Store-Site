from flask import Blueprint, render_template, request, flash, redirect, url_for,session
from flask_login import login_user, login_required, logout_user, current_user
from flask import current_app as app
from application.models import *
from application.database import db
from werkzeug.security import check_password_hash
from application.views.auth import check_address
import requests
from datetime import datetime

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




@viewsCustomer.route('/customer/<int:c_id>/past_orders')
def past_orders(c_id):
    return render_template("userviews/customer/pastOrders.html", c_id=c_id,orders=OrderDetails.query.filter_by(customer_id=c_id).all())

@viewsCustomer.route('/customer/<int:c_id>/order/<int:order_id>')
def order_details(c_id,order_id):
    orderItems=OrdersItems.query.filter_by(order_id=order_id).all()
    order=OrderDetails.query.filter_by(order_id=order_id).first()
    total_price=order.total_price
    products=[]
    for item in orderItems:
        base_url = request.host_url[:-1]
        response = requests.get(f'{base_url}/products/{item.product_id}')
        product=response.json()
        pname=product['name']
        products.append({'cart_quantity':item.quantity,'price':item.price,'name':pname})
    return render_template("userviews/customer/orderDetails.html", c_id=c_id,products=products,total_price=total_price,delivery_status=order.delivery_status,order_id=order_id)




@viewsCustomer.route('/customer/<int:c_id>/searchProducts', methods=['GET', 'POST'])
def searchProducts(c_id):
    base_url = request.host_url[:-1]
    response = requests.get(f'{base_url}/categories')
    categories=response.json()
    if request.method == 'POST':
        name=request.form.get('name')
        category_id=request.form.get('category')
        min_price=request.form.get('min_price')
        max_price=request.form.get('max_price')
        min_manufacture_date=request.form.get('min_manufacture_date')
        max_manufacture_date=request.form.get('max_manufacture_date')
        min_expiry_date=request.form.get('min_expiry_date')
        max_expiry_date=request.form.get('max_expiry_date')
        if category_id=='all':
            response = requests.get(f'{base_url}/products')
        else:
            response = requests.get(f'{base_url}/products/1/{category_id}')
        products=response.json()
        if name!='':
            products=[product for product in products if name.lower() in product['name'].lower()]
        if (min_price!='' and max_price=='') or (min_price=='' and max_price!=''):
            if min_price=='': min_price=0
            if max_price=='': max_price=100000000
            products=[product for product in products if float(product['price'])>=float(min_price) and float(product['price'])<=float(max_price)]
        if (min_manufacture_date!='' and max_manufacture_date=='') or (min_manufacture_date=='' and max_manufacture_date!=''):
            if min_manufacture_date=='': min_manufacture_date='01-01-0001'
            if max_manufacture_date=='': max_manufacture_date='31-12-9999'
            products=[product for product in products if product['manufacture_date']>=min_manufacture_date and product['manufacture_date']<=max_manufacture_date]
        if (min_expiry_date!='' and max_expiry_date=='') or (min_expiry_date=='' and max_expiry_date!=''):
            if min_expiry_date=='': min_expiry_date='01-01-0001'
            if max_expiry_date=='': max_expiry_date='31-12-9999'
            products=[product for product in products if product['expiry_date']>=min_expiry_date and product['expiry_date']<=max_expiry_date]
        return render_template("userviews/customer/searchResults.html",c_id=c_id,products=products)
    return render_template("userviews/customer/searchProducts.html",categories=categories,c_id=c_id)

@viewsCustomer.route('/customer/<int:c_id>/searchResults', methods=['GET', 'POST'])
def searchResults(c_id):
    if request.method=='POST':
        quantity = request.form.get('quantity')
        product_id = request.form.get('product_id')
        c_id= request.form.get('c_id')
        if Cart.query.filter_by(customer_id=c_id,product_id=product_id).first():
            cart=Cart.query.filter_by(customer_id=c_id,product_id=product_id).first()
            cart.quantity+=int(quantity)
            db.session.commit()
        else:
            cart=Cart(customer_id=c_id,product_id=product_id,quantity=quantity)
            db.session.add(cart)
            db.session.commit()
        return redirect(url_for("viewsCustomer.cart",c_id=c_id))
    return redirect(url_for("viewsCustomer.searchProducts",c_id=c_id))





@viewsCustomer.route('/customer/<int:c_id>/cart', methods=['GET', 'POST'])
def cart(c_id):
    if request.method == 'GET':
        base_url = request.host_url[:-1]
        products=[]
        cart=Cart.query.filter_by(customer_id=c_id).all()
        for product in cart:
            id=product.product_id
            response = requests.get(f'{base_url}/products/{id}')
            cart_item=response.json()
            cart_item['cart_quantity']=product.quantity
            products.append(cart_item)
        total_price=getTotalPrice(products)
        return render_template("userviews/customer/goToCart.html", c_id=c_id, products=products,total_price=total_price)
    
    if request.method == 'POST':
        m=False
        products=eval(request.form.get('products')) #cart_products
        total_price=request.form.get('total_price')
        for i in products:
            if (i['cart_quantity']*(i['price']/i['pricePerUnit']))>i['quantity']:
                flash(f'Only {str(i["quantity"])} {i["unit"]} of {i["name"]} is available in stock. Please remove the extra units from your cart to proceed.', category='error')
                m=True
                #return render_template("userviews/customer/goToCart.html", c_id=c_id, products=products,total_price=total_price)
            elif i['quantity']==0:
                flash(f'{i["name"]} is out of stock. Please remove it from your cart to proceed.', category='error')
                m=True
                #return render_template("userviews/customer/goToCart.html", c_id=c_id, products=products,total_price=total_price)
        if not m:
            customer=Customer.query.filter_by(customer_id=c_id).first()
            name=customer.name
            address=customer.address
            phone=customer.phone_no
            total_price=request.form.get('total_price')
            products=eval(request.form.get('products'))
            return render_template("userviews/customer/orderPreview.html",c_id=c_id,name=name,address=address,phone=phone,products=products,total_price=total_price)
        return render_template("userviews/customer/goToCart.html", c_id=c_id, products=products,total_price=total_price)
    
def getTotalPrice(products):
    tp=0
    for product in products:
        tp+=(float(product['cart_quantity'])*float(product['price']))
    return round(tp,2)

@viewsCustomer.route('/customer/<int:c_id>/removeFromCart/<int:p_id>')
def removeFromCart(c_id,p_id):
    sno=Cart.query.filter_by(customer_id=c_id,product_id=p_id).first().sno
    db.session.delete(Cart.query.filter_by(sno=sno).first())
    db.session.commit()
    return redirect(url_for('viewsCustomer.cart',c_id=c_id))






    
#use a payment gateway instead
@viewsCustomer.route('/customer/<int:c_id>/placeOrder/<float:total_price>', methods=['GET', 'POST'])
def placeOrder(c_id,total_price):
    new_order=OrderDetails(customer_id=c_id,branch_id=1,delivery_executive_id=delivery_executive_assign(len(OrderDetails.query.all())),delivery_status='ORDER PLACED',order_date=datetime.now(),total_price=total_price)
    db.session.add(new_order)
    db.session.commit()
    order_id=new_order.order_id
    cart_items=Cart.query.filter_by(customer_id=c_id).all()
    for cart_item in cart_items:
        product_id=cart_item.product_id
        quantity=cart_item.quantity
        base_url = request.host_url[:-1]
        response = requests.get(f'{base_url}/products/{product_id}')
        product=response.json()
        new_order_item=OrdersItems(order_id=order_id,product_id=product_id,quantity=quantity,price=product['price']) 
        db.session.add(new_order_item)
        db.session.commit()
        #reducing stock quantity
        new_quantity=product['quantity']-(quantity*(product['price']/product['pricePerUnit']))
        product['quantity']=new_quantity
        response=requests.put(f'{base_url}/products/{product_id}',json=product)
    for cart_item in cart_items:
        db.session.delete(cart_item)
        db.session.commit()
    return redirect(url_for('viewsCustomer.past_orders',c_id=c_id))

def delivery_executive_assign(n):
    return (n+1)%3