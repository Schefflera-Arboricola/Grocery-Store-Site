from .database import db

'''
customer : customer_id, name, email, username, hpassword, phone no, address, cart_id
app manager : appmgr_id, name, email, username, hpassword, phone no, address, permissions
store manager : store_id, name, email, username, hpassword, phone no, address, inventory management permissions
orders_items : order_id(not a pri key), price, quantity
oder_details: order_id, customer_id, store_id, delivery_details
Category : category_id, name, description, store_id
products : product_id, name, description, price, quantity, store_id, category, manufacture date, expiry date
cart: cart_id, product_id, quantity, total_price
payment: payment_id, order_id, payment_method, payment_status, payment_date, payment_amount
PasswordReset : token, email, username, expiration time, role
'''

class Customer(db.Model):
    __tablename__='customer'
    customer_id=db.Column(db.Integer, autoincrement=True,primary_key=True)
    name=db.Column(db.String)
    email=db.Column(db.String,unique=True)
    username=db.Column(db.String,unique=True)
    hpassword=db.Column(db.String)
    phone_no=db.Column(db.String)
    address=db.Column(db.String)
    cart_id=db.Column(db.Integer, db.ForeignKey("cart.cart_id"),nullable=False)

class AppManager(db.Model):
    __tablename__='app_manager'
    appmgr_id=db.Column(db.Integer, autoincrement=True,primary_key=True)
    name=db.Column(db.String)
    email=db.Column(db.String,unique=True)
    username=db.Column(db.String,unique=True)
    hpassword=db.Column(db.String)
    phone_no=db.Column(db.String)
    address=db.Column(db.String)
    permissions=db.Column(db.String)

class StoreManager(db.Model):
    __tablename__='store_manager'
    store_id=db.Column(db.Integer, autoincrement=True,primary_key=True)
    name=db.Column(db.String)
    email=db.Column(db.String,unique=True)
    username=db.Column(db.String,unique=True)
    hpassword=db.Column(db.String)
    phone_no=db.Column(db.String)
    address=db.Column(db.String)
    permissions=db.Column(db.String)

class OrderDetails(db.Model):
    __tablename__='order_details'
    order_id=db.Column(db.Integer, autoincrement=True,primary_key=True)
    customer_id=db.Column(db.Integer, db.ForeignKey("customer.customer_id"),nullable=False)
    store_id=db.Column(db.Integer, db.ForeignKey("store_manager.store_id"),nullable=False)
    delivery_details=db.Column(db.String)
    
class OrdersItems(db.Model):
    __tablename__='orders_items'
    order_id=db.Column(db.Integer, db.ForeignKey("order_details.order_id"),primary_key=True,nullable=False)
    price=db.Column(db.String)
    quantity=db.Column(db.Integer)

class Category(db.Model):
    __tablename__='category'
    category_id=db.Column(db.Integer, autoincrement=True,primary_key=True)
    name=db.Column(db.String)
    description=db.Column(db.String)
    store_id=db.Column(db.Integer, db.ForeignKey("store_manager.store_id"),nullable=False)
    
class Products(db.Model):
    __tablename__='products'
    product_id=db.Column(db.Integer, autoincrement=True,primary_key=True)
    name=db.Column(db.String)
    description=db.Column(db.String)
    price=db.Column(db.String)
    quantity=db.Column(db.Integer)
    store_id=db.Column(db.Integer, db.ForeignKey("store_manager.store_id"),nullable=False)
    category_id=db.Column(db.Integer, db.ForeignKey("category.category_id"),nullable=False)
    manufacture_date=db.Column(db.Date)
    expiry_date=db.Column(db.Date)

class Cart(db.Model):
    __tablename__='cart'
    cart_id=db.Column(db.Integer, autoincrement=True,primary_key=True)
    product_id=db.Column(db.Integer, db.ForeignKey("products.product_id"),nullable=False)
    quantity=db.Column(db.Integer)

class Payment(db.Model):
    __tablename__='payment'
    payment_id=db.Column(db.Integer, autoincrement=True,primary_key=True)
    order_id=db.Column(db.Integer, db.ForeignKey("order_details.order_id"),nullable=False)
    payment_method=db.Column(db.String)
    payment_status=db.Column(db.String)
    payment_date=db.Column(db.String)
    payment_amount=db.Column(db.String)

class PasswordReset(db.Model):
    __tablename__='password_reset'
    token=db.Column(db.String, primary_key=True)
    email = db.Column(db.String, unique=True)
    expiration_time = db.Column(db.DateTime)

db.create_all()

