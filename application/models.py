from .database import db
from flask_login import UserMixin

'''
customer: customer_id (pri), name, email (uni), username (uni), hpassword, phone_no (uni), address, cart_id (foreign)
branch: branch_id (pri), location, phone_no
store_manager: store_manager_id (pri), name, email (uni), hpassword, phone_no, branch_id (foreign)
delivery_executive: delivery_executive_id (pri), name, email (uni), hpassword, phone_no, branch_id (foreign)
category: category_id (pri), name, description
products: product_id (pri), name, description, price, quantity, branch_id (foreign), category_id (foreign), manufacture_date, expiry_date
cart: cart_id (pri), product_id (foreign), quantity
payment: payment_id (pri), customer_id (foreign), payment_status, payment_date
order_details: order_id (pri), customer_id (foreign), branch_id (foreign), delivery_executive_id (foreign), payment_id (foreign), delivery_status
orders_items: order_id (foreign), price, quantity
password_reset: token (pri), email (uni), expiration_time
'''


class User(db.Model,UserMixin):
    __abstract__=True
    name=db.Column(db.String,nullable=False)
    email=db.Column(db.String,unique=True,nullable=False)
    username=db.Column(db.String,unique=True,nullable=False)
    password=db.Column(db.String,nullable=False)
    phone_no=db.Column(db.String,nullable=False)

#when a new customer signups we need to make a cart(generate art_id) for them that is empty
class Customer(User):
    __tablename__='customer'
    customer_id=db.Column(db.Integer, autoincrement=True,primary_key=True)
    address=db.Column(db.String,nullable=False)
    def get_id(self):
        return str(self.customer_id)

#unique store_manager_id is assigned by the store admin to all managers, using which they can sign up and sign in
#same for delievery executives
class StoreManager(User):
    __tablename__='store_manager'
    store_manager_id=db.Column(db.Integer, autoincrement=True,primary_key=True)
    #branch_id=db.Column(db.Integer, db.ForeignKey("branch.branch_id"),nullable=False)
    def get_id(self):
        return str(self.store_manager_id)

class DeliveryExecutive(User):
    __tablename__='delivery_executive'
    delivery_executive_id=db.Column(db.Integer, autoincrement=True,primary_key=True)
    #branch_id=db.Column(db.Integer, db.ForeignKey("branch.branch_id"),nullable=False)
    def get_id(self):
        return str(self.delivery_executive_id)
'''
#one store can have different branches with multiple store managers
class Branch(db.Model):
    __tablename__='branch'
    branch_id=db.Column(db.Integer,autoincrement=True,primary_key=True)
    location=db.Column(db.String,nullable=False)
    phone_no=db.Column(db.String)

    
#generated by store, and checked from here if the id used while signup are correct

class StoreManager(db.Model):
    __tablename__='store_manager_ids'
    store_manager_id=db.Column(db.Integer, autoincrement=True,primary_key=True) 
    branch_id=db.Column(db.Integer, db.ForeignKey("branch.branch_id"),nullable=False)

class DeliveryExecutive(db.Model):
    __tablename__='delivery_executive_ids'
    delivery_executive_id=db.Column(db.Integer, autoincrement=True,primary_key=True)
    branch_id=db.Column(db.Integer, db.ForeignKey("branch.branch_id"),nullable=False)

'''
class Category(db.Model):
    __tablename__='category'
    category_id=db.Column(db.Integer, autoincrement=True,primary_key=True)
    name=db.Column(db.String)
    description=db.Column(db.String)
    
class Products(db.Model):
    __tablename__='products'
    product_id=db.Column(db.Integer, autoincrement=True,primary_key=True)
    name=db.Column(db.String)
    description=db.Column(db.String)
    price=db.Column(db.String)
    quantity=db.Column(db.Integer)
    #branch_id=db.Column(db.Integer, db.ForeignKey("branch.branch_id"),nullable=False)
    category_id=db.Column(db.Integer, db.ForeignKey("category.category_id"),nullable=False)
    manufacture_date=db.Column(db.Date)
    expiry_date=db.Column(db.Date)

class Cart(db.Model):
    __tablename__='cart'
    sno=db.Column(db.Integer, autoincrement=True,primary_key=True)
    customer_id=db.Column(db.Integer, db.ForeignKey("customer.customer_id"),nullable=False)
    product_id=db.Column(db.Integer, db.ForeignKey("products.product_id"))
    quantity=db.Column(db.Integer)

#once the payment is done(i.e. payment_status='Successful') the cart gets emptied and all the items in cart goes to orders_items table
class Payment(db.Model):
    __tablename__='payment'
    payment_id=db.Column(db.Integer, autoincrement=True,primary_key=True)
    customer_id=db.Column(db.Integer, db.ForeignKey("customer.customer_id"),nullable=False)
    payment_status=db.Column(db.String)
    payment_date=db.Column(db.String)

class OrderDetails(db.Model):
    __tablename__='order_details'
    order_id=db.Column(db.Integer, autoincrement=True,primary_key=True)
    customer_id=db.Column(db.Integer, db.ForeignKey("customer.customer_id"),nullable=False)
    #branch_id=db.Column(db.Integer, db.ForeignKey("branch.branch_id"),nullable=False)
    delivery_executive_id=db.Column(db.Integer, db.ForeignKey("delivery_executive.delivery_executive_id"),nullable=False)
    payment_id=db.Column(db.Integer, db.ForeignKey("payment.payment_id"),nullable=False)
    delivery_status=db.Column(db.String)

class OrdersItems(db.Model):
    __tablename__='orders_items'
    sno=db.Column(db.Integer, autoincrement=True,primary_key=True)
    order_id=db.Column(db.Integer, db.ForeignKey("order_details.order_id"),nullable=False)
    price=db.Column(db.String)
    quantity=db.Column(db.Integer)

class PasswordReset(db.Model):
    __tablename__='password_reset'
    token=db.Column(db.String, primary_key=True)
    email = db.Column(db.String, unique=True)
    expiration_time = db.Column(db.DateTime)

db.create_all()