from database import db

'''
customer : customer_id, name, email, password, phone no, address, cart_id
app manager : appmgr_id, name, email, password, phone no, address, permissions
store manager : store_id, name, email, password, phone no, address, inventory management permissions
orders_items : order_id(not a pri key), price, quantity
oder_details: order_id, customer_id, store_id, delivery_details
products : product_id, name, description, price, quantity, store_id, tags
cart: cart_id, product_id, quantity, total_price
payment: payment_id, order_id, payment_method, payment_status, payment_date, payment_amount
'''

class Customer(db.Model):
    __tablename__='customer'
    customer_id=db.Column(db.Integer, autoincrement=True,primary_key=True)
    name=db.Column(db.String)
    email=db.Column(db.String,unique=True)
    password=db.Column(db.String)
    phone_no=db.Column(db.String)
    address=db.Column(db.String)
    cart_id=db.Column(db.Integer, db.ForeignKey("cart.cart_id"),nullable=False)

class AppManager(db.Model):
    __tablename__='app_manager'
    appmgr_id=db.Column(db.Integer, autoincrement=True,primary_key=True)
    name=db.Column(db.String)
    email=db.Column(db.String,unique=True)
    password=db.Column(db.String)
    phone_no=db.Column(db.String)
    address=db.Column(db.String)
    permissions=db.Column(db.String)

class StoreManager(db.Model):
    __tablename__='store_manager'
    store_id=db.Column(db.Integer, autoincrement=True,primary_key=True)
    name=db.Column(db.String)
    email=db.Column(db.String,unique=True)
    password=db.Column(db.String)
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

class Products(db.Model):
    __tablename__='products'
    product_id=db.Column(db.Integer, autoincrement=True,primary_key=True)
    name=db.Column(db.String)
    description=db.Column(db.String)
    price=db.Column(db.String)
    quantity=db.Column(db.Integer)
    store_id=db.Column(db.Integer, db.ForeignKey("store_manager.store_id"),nullable=False)
    tags=db.Column(db.String)

class Cart(db.Model):
    __tablename__='cart'
    cart_id=db.Column(db.Integer, autoincrement=True,primary_key=True)
    product_id=db.Column(db.Integer, db.ForeignKey("products.product_id"),nullable=False)
    quantity=db.Column(db.Integer)
    total_price=db.Column(db.Ineger)

class Payment(db.Model):
    __tablename__='payment'
    payment_id=db.Column(db.Integer, autoincrement=True,primary_key=True)
    order_id=db.Column(db.Integer, db.ForeignKey("order_details.order_id"),nullable=False)
    payment_method=db.Column(db.String)
    payment_status=db.Column(db.String)
    payment_date=db.Column(db.String)
    payment_amount=db.Column(db.String)

db.create_all()
