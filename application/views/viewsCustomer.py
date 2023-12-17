from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_required, current_user
from flask import current_app as app
from application.models import *
from application.database import db
from werkzeug.security import check_password_hash
from application.views.auth import check_address
from datetime import datetime
import stripe
from ML_models import similarProducts, recommender
from sqlalchemy import desc
from db_directory.accessDB import *
from application.config import cache

viewsCustomer = Blueprint("viewsCustomer", __name__)

# Apply the login_required decorator to all routes in the viewsCustomer blueprint
@viewsCustomer.before_request
@login_required
def require_login():
    customer_id = request.view_args.get("c_id")
    if (
        not isinstance(current_user, Customer)
        or current_user.customer_id != customer_id
    ):
        return render_template("error.html"), 401
    else:
        if request.method in "GET":
            current_user.last_login = datetime.now()
            db.session.commit()


@viewsCustomer.route("/customer/<int:c_id>/dashboard")
@cache.cached(timeout=20)
def dashboard(c_id):
    user = Customer.query.filter_by(customer_id=c_id).first()
    products, status_code = GetProduct()
    categories, status_code = GetCategory()

    total_orders = OrderDetails.query.filter_by(customer_id=c_id).count()
    n = 5  # number of past orders to be considered for recommendation
    if total_orders >= n:
        orders = (
            OrderDetails.query.filter_by(customer_id=c_id)
            .order_by(desc(OrderDetails.order_date))
            .limit(n)
            .all()
        )
    else:
        orders = OrderDetails.query.filter_by(customer_id=c_id).all()
    orderItems = []
    for order in orders:
        items = OrdersItems.query.filter_by(order_id=order.order_id).all()
        for item in items:
            if Products.query.get(item.product_id).isDeleted != "True":
                item_dict = {
                    "order_id": order.order_id,
                    "sno": item.sno,
                    "product_id": item.product_id,
                    "order_date": order.order_date,
                    "price": item.price,
                    "quantity": item.quantity,
                }
                orderItems.append(item_dict)
    if orderItems == []:
        products = None
    else:
        products = recommender.recommendProducts(products, categories, orderItems)
    return render_template(
        "dashboard/dashboard_customer.html",
        account_type="customer",
        id=c_id,
        name=user.name,
        address=user.address,
        phone=user.phone_no,
        username=user.username,
        email=user.email,
        products=products,
    )


@viewsCustomer.route("/customer/<int:c_id>/editProfile", methods=["GET", "POST"])
def editProfile(c_id):
    if request.method == "POST":
        name = request.form.get("name")
        phone = request.form.get("phone")
        address = request.form.get("address")
        password = request.form.get("password")
        user = Customer.query.filter_by(customer_id=c_id).first()
        user.name = name
        user.phone_no = phone
        user.address = address
        if check_password_hash(user.password, password):
            features = check_user_features(name, phone)
            add = check_address(address)
            if features != True:
                flash(features, category="error")
                return render_template(
                    "editProfile/editProfile_customer.html",
                    name=user.name,
                    phone=user.phone_no,
                    address=user.address,
                )
            elif add != True:
                flash(add, category="error")
                return render_template(
                    "editProfile/editProfile_customer.html",
                    name=user.name,
                    phone=user.phone_no,
                    address=user.address,
                )
            else:
                db.session.commit()
                return redirect(url_for("viewsCustomer.dashboard", c_id=c_id))
        else:
            flash("Incorrect password, try again.", category="error")
            return render_template(
                "editProfile/editProfile_customer.html",
                name=user.name,
                address=user.address,
                phone=user.phone_no,
            )
    else:
        user = Customer.query.filter_by(customer_id=c_id).first()
        return render_template(
            "editProfile/editProfile_customer.html",
            name=user.name,
            address=user.address,
            phone=user.phone_no,
        )


def check_user_features(name, phone):
    if len(phone) != 10 and phone.isdigit():
        return "Phone number must have 10 digits"
    elif type(name) != str:
        return "Name must be a string"
    else:
        return True


@viewsCustomer.route("/customer/<int:c_id>/past_orders")
def past_orders(c_id):
    return render_template(
        "userviews/customer/pastOrders.html",
        c_id=c_id,
        orders=OrderDetails.query.filter_by(customer_id=c_id).all(),
    )


@viewsCustomer.route("/customer/<int:c_id>/order/<int:order_id>")
def order_details(c_id, order_id):
    orderItems = OrdersItems.query.filter_by(order_id=order_id).all()
    order = OrderDetails.query.filter_by(order_id=order_id).first()
    total_price = order.total_price
    products = []
    for item in orderItems:
        product = Products.query.get(item.product_id)
        pname = product.name
        products.append(
            {"cart_quantity": item.quantity, "price": item.price, "name": pname}
        )
    return render_template(
        "userviews/customer/orderDetails.html",
        c_id=c_id,
        products=products,
        total_price=total_price,
        delivery_status=order.delivery_status,
        order_id=order_id,
        modeOfPayment=order.modeOfPayment,
        order_date=order.order_date,
    )


@viewsCustomer.route("/customer/<int:c_id>/searchProducts", methods=["GET", "POST"])
def searchProducts(c_id):
    categories, status_code = GetCategory()
    if request.method == "POST":
        name = request.form.get("name")
        category_id = request.form.get("category")
        min_price = request.form.get("min_price")
        max_price = request.form.get("max_price")
        min_avg_rating = request.form.get("min_avg_rating")
        max_avg_rating = request.form.get("max_avg_rating")
        min_manufacture_date = request.form.get("min_manufacture_date")
        max_manufacture_date = request.form.get("max_manufacture_date")
        min_expiry_date = request.form.get("min_expiry_date")
        max_expiry_date = request.form.get("max_expiry_date")
        if category_id == "all":
            products, status_code = GetProduct()
        else:
            products, status_code = GetProduct(flag=1, category_id=category_id)
        if name != "":
            products = [
                product
                for product in products
                if name.lower() in product["name"].lower()
            ]
        if (min_price != "" and max_price == "") or (
            min_price == "" and max_price != ""
        ):
            if min_price == "":
                min_price = 0
            if max_price == "":
                max_price = 100000000
            products = [
                product
                for product in products
                if float(product["price"]) >= float(min_price)
                and float(product["price"]) <= float(max_price)
            ]
        if (min_avg_rating != "" and max_avg_rating == "") or (
            min_avg_rating == "" and max_avg_rating != ""
        ):
            if min_avg_rating == "":
                min_avg_rating = 0
            if max_avg_rating == "":
                max_avg_rating = 5
            products = [
                product
                for product in products
                if product["avg_rating"] != None
                and float(product["avg_rating"]) >= float(min_avg_rating)
                and float(product["avg_rating"]) <= float(max_avg_rating)
            ]
        if (min_manufacture_date != "" and max_manufacture_date == "") or (
            min_manufacture_date == "" and max_manufacture_date != ""
        ):
            if min_manufacture_date == "":
                min_manufacture_date = "01-01-0001"
            if max_manufacture_date == "":
                max_manufacture_date = "31-12-9999"
            products = [
                product
                for product in products
                if product["manufacture_date"] >= min_manufacture_date
                and product["manufacture_date"] <= max_manufacture_date
            ]
        if (min_expiry_date != "" and max_expiry_date == "") or (
            min_expiry_date == "" and max_expiry_date != ""
        ):
            if min_expiry_date == "":
                min_expiry_date = "01-01-0001"
            if max_expiry_date == "":
                max_expiry_date = "31-12-9999"
            products = [
                product
                for product in products
                if product["expiry_date"] >= min_expiry_date
                and product["expiry_date"] <= max_expiry_date
            ]
        return render_template(
            "userviews/customer/searchResults.html", c_id=c_id, products=products
        )
    return render_template(
        "userviews/customer/searchProducts.html", categories=categories, c_id=c_id
    )


@viewsCustomer.route("/customer/<int:c_id>/searchResults", methods=["GET", "POST"])
def searchResults(c_id):
    if request.method == "POST":
        quantity = int(request.form.get("quantity"))
        product_id = request.form.get("product_id")
        c_id = request.form.get("c_id")
        if Cart.query.filter_by(customer_id=c_id, product_id=product_id).first():
            cart = Cart.query.filter_by(customer_id=c_id, product_id=product_id).first()
            cart.quantity += int(quantity)
            db.session.commit()
        else:
            cart = Cart(customer_id=c_id, product_id=product_id, quantity=quantity)
            db.session.add(cart)
            db.session.commit()
        return redirect(url_for("viewsCustomer.cart", c_id=c_id))
    return redirect(url_for("viewsCustomer.searchProducts", c_id=c_id))


@viewsCustomer.route(
    "/customer/<int:c_id>/productDetails/<int:product_id>", methods=["GET", "POST"]
)
def productDetails(c_id, product_id):
    if request.method == "GET":
        reviews = Reviews.query.filter_by(product_id=product_id).all()
        categories, status_code = GetCategory()
        all_products, status_code = GetProduct()
        product, status_code = GetProduct(product_id)
        similar_products = similarProducts.similarProducts(
            product, all_products, categories
        )
        return render_template(
            "userviews/customer/productDetails.html",
            c_id=c_id,
            product=product,
            reviews=reviews,
            similar_products=similar_products,
        )
    if request.method == "POST":
        rating = request.form.get("rating")
        review_text = request.form.get("review_text")
        date = datetime.now().strftime("%d-%m-%Y")
        isPurchased = False
        for i in OrderDetails.query.filter_by(customer_id=c_id).all():
            flag = False
            for j in OrdersItems.query.filter_by(order_id=i.order_id).all():
                if j.product_id == product_id:
                    isPurchased, flag = True, True
                    break
            if flag:
                break
        updateRating(product_id, rating)
        review = Reviews(
            customer_id=c_id,
            product_id=product_id,
            stars=rating,
            review_text=review_text,
            date=date,
            isPurchased=isPurchased,
        )
        db.session.add(review)
        db.session.commit()
        return redirect(
            url_for("viewsCustomer.productDetails", c_id=c_id, product_id=product_id)
        )


def updateRating(product_id, rating):
    product_info, status_code = GetProduct(product_id)
    if product_info["avg_rating"] is None:
        product_info["avg_rating"] = int(rating)
    else:
        reviews = Reviews.query.filter_by(product_id=product_id).all()
        count = len(reviews)
        avg_rating = round(
            (float(product_info["avg_rating"]) * count + int(rating)) / (count + 1), 2
        )
        product_info["avg_rating"] = avg_rating
    response, status_code = UpdateProduct(product_id, data=product_info)


@viewsCustomer.route("/customer/<int:c_id>/cart", methods=["GET", "POST"])
def cart(c_id):
    if request.method == "GET":
        products = []
        cart = Cart.query.filter_by(customer_id=c_id).all()
        for product in cart:
            prod_id = product.product_id
            cart_item, status_code = GetProduct(prod_id)
            if status_code == 200:
                cart_item["cart_quantity"] = product.quantity
                products.append(cart_item)
            elif status_code == 404 and cart_item["message"] == "Product was deleted":
                prod_name = Products.query.get(prod_id).name
                db.session.delete(product)
                db.session.commit()
                flash(f"{prod_name} is not available anymore.", category="error")
        total_price = getTotalPrice(products)
        return render_template(
            "userviews/customer/goToCart.html",
            c_id=c_id,
            products=products,
            total_price=total_price,
        )

    if request.method == "POST":  # checkout
        m = False
        products = eval(request.form.get("products"))  # cart_products
        total_price = request.form.get("total_price")
        if len(products) == 0:
            flash(
                "Your cart is empty. Please add some products to your cart to proceed.",
                category="error",
            )
            m = True
        for i in products:
            if (i["cart_quantity"] * (i["price"] / i["pricePerUnit"])) > i["quantity"]:
                flash(
                    f'Only {str(i["quantity"])} {i["unit"]} of {i["name"]} is available in stock. Please remove the extra units from your cart to proceed.',
                    category="error",
                )
                m = True
            elif i["quantity"] == 0:
                flash(
                    f'{i["name"]} is out of stock. Please remove it from your cart to proceed.',
                    category="error",
                )
                m = True
        if not m:
            customer = Customer.query.filter_by(customer_id=c_id).first()
            name = customer.name
            address = customer.address
            phone = customer.phone_no
            total_price = request.form.get("total_price")
            products = eval(request.form.get("products"))
            return render_template(
                "userviews/customer/orderPreview.html",
                c_id=c_id,
                name=name,
                address=address,
                phone=phone,
                products=products,
                total_price=total_price,
            )
        return render_template(
            "userviews/customer/goToCart.html",
            c_id=c_id,
            products=products,
            total_price=total_price,
        )


def getTotalPrice(products):
    tp = 0
    for product in products:
        tp += float(product["cart_quantity"]) * float(product["price"])
    return round(tp, 2)


@viewsCustomer.route("/customer/<int:c_id>/removeFromCart/<int:p_id>")
def removeFromCart(c_id, p_id):
    sno = Cart.query.filter_by(customer_id=c_id, product_id=p_id).first().sno
    db.session.delete(Cart.query.filter_by(sno=sno).first())
    db.session.commit()
    return redirect(url_for("viewsCustomer.cart", c_id=c_id))


@viewsCustomer.route(
    "/customer/<int:c_id>/placeOrder/<float:total_price>", methods=["GET", "POST"]
)
def placeOrder(c_id, total_price):
    if request.method == "POST":
        mode = request.form.get("payment_mode")
        if mode == "cod":
            placeorder(c_id, total_price, "Cash on Delivery")
            return redirect(url_for("viewsCustomer.past_orders", c_id=c_id))
        elif mode == "online":
            return redirect(
                url_for("viewsCustomer.paynow", c_id=c_id, total_price=total_price)
            )
        else:
            return "error : contact admin"


@viewsCustomer.route(
    "/customer/<int:c_id>/paynow/<float:total_price>", methods=["GET", "POST"]
)
def paynow(c_id, total_price):
    stripe.api_key = app.config["STRIPE_SECRET_KEY"]
    stripe_public_key = app.config["STRIPE_PUBLIC_KEY"]
    # Create a Stripe Payment Intent
    tp = int(total_price) * 100  # in paise
    payment_intent = stripe.PaymentIntent.create(
        amount=tp, currency="inr", payment_method_types=["card"]
    )
    # Update the user's payment status in your database
    new_payment = onlinePayments(
        customer_id=c_id,
        payment_amount=total_price,
        order_id="NULL",
        payment_intent_id=payment_intent.id,
        payment_status="pending",
        payment_date=datetime.now(),
    )
    db.session.add(new_payment)
    db.session.commit()
    return render_template(
        "userviews/customer/checkout.html",
        client_secret=payment_intent.client_secret,
        stripe_public_key=stripe_public_key,
        total_price=total_price,
        c_id=c_id,
    )


@viewsCustomer.route("/customer/<int:c_id>/payment_failure/<float:total_price>")
def payment_failure(c_id, total_price):
    placeorder(c_id, total_price, "Cash on Delivery")
    db.session.commit()
    return redirect(url_for("viewsCustomer.past_orders", c_id=c_id))


@viewsCustomer.route("/customer/<int:c_id>/payment_success/<float:total_price>")
def payment_success(c_id, total_price):
    try:
        payment = (
            onlinePayments.query.filter_by(customer_id=c_id)
            .order_by(onlinePayments.payment_id.desc())
            .first()
        )
        if payment:
            placeorder(c_id, total_price, "Online")
            payment.payment_status = "paid"
            payment.order_id = (
                OrderDetails.query.filter_by(customer_id=c_id)
                .order_by(OrderDetails.order_id.desc())
                .first()
                .order_id
            )
            db.session.commit()
            return redirect(url_for("viewsCustomer.past_orders", c_id=c_id))
    except Exception as e:
        print(e)
        return "", 400


stripe.api_key = app.config["STRIPE_SECRET_KEY"]


@viewsCustomer.route("/webhook", methods=["POST"])
def webhook():
    payload = request.get_json()
    event = None
    try:
        event = stripe.Event.construct_from(payload, stripe.api_key)
    except ValueError as e:
        # Invalid payload
        print(f"error : {e}")
        return "", 400
    # Handle the event based on its type
    if event.type == "payment_intent.succeeded":
        return "", 200
    else:
        print(f"error : {event.type}")
        return "", 400


def placeorder(c_id, total_price, payment_mode):
    # adding order to order_details table
    new_order = OrderDetails(
        customer_id=c_id,
        branch_id=1,
        delivery_executive_id=delivery_executive_assign(len(OrderDetails.query.all())),
        delivery_status="ORDER PLACED",
        order_date=datetime.now(),
        total_price=total_price,
        modeOfPayment=payment_mode,
    )
    db.session.add(new_order)
    db.session.commit()

    # transfering cart items to order_items table and reducing stock quantity
    order_id = new_order.order_id
    cart_items = Cart.query.filter_by(customer_id=c_id).all()
    for cart_item in cart_items:
        product_id = cart_item.product_id
        quantity = cart_item.quantity
        product, status_code = GetProduct(product_id)
        new_order_item = OrdersItems(
            order_id=order_id,
            product_id=product_id,
            quantity=quantity,
            price=product["price"],
        )
        db.session.add(new_order_item)
        db.session.commit()
        # reducing stock quantity
        new_quantity = product["quantity"] - (
            quantity * (product["price"] / product["pricePerUnit"])
        )
        product["quantity"] = new_quantity
        response, status_code = UpdateProduct(product_id, data=product)

    # emptying the cart
    for cart_item in cart_items:
        db.session.delete(cart_item)
        db.session.commit()


def delivery_executive_assign(n):
    return (n + 1) % 3
