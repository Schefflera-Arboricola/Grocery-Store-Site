from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import (
    login_user,
    login_required,
    logout_user,
    LoginManager,
    current_user,
)
from flask import current_app as app
from application.models import *
from application.database import db
from werkzeug.security import generate_password_hash, check_password_hash
from application.views.viewsDelExe import generateOTP, sendOTP
from flask_jwt_extended import create_access_token

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    if "account_type" not in session:
        session["account_type"] = "user"
        return render_template("signinup/signin_base.html")
    if session["account_type"] == "Customer":
        return Customer.query.get(int(user_id))
    elif session["account_type"] == "Admin":
        return Admin.query.get(int(user_id))
    elif session["account_type"] == "StoreManager":
        return StoreManager.query.get(int(user_id))
    elif session["account_type"] == "DeliveryExecutive":
        return DeliveryExecutive.query.get(int(user_id))
    elif session["account_type"] == "developer":
        return Developer.query.get(int(user_id))
    else:
        return None


auth = Blueprint("auth", __name__)


# Signin route


@auth.route("/", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get("role")
        if role == "customer":
            user = Customer.query.filter_by(username=username).first()
        elif role == "admin":
            user = Admin.query.filter_by(username=username).first()
        elif role == "store-manager":
            user = StoreManager.query.filter_by(username=username).first()
        elif role == "delivery-executive":
            user = DeliveryExecutive.query.filter_by(username=username).first()
        elif role == "developer":
            user = Developer.query.filter_by(username=username).first()
        else:
            flash(
                "Please select a role before proceeding to sign in.", category="error"
            )
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                if role == "customer":
                    session["account_type"] = "Customer"
                    return redirect(
                        url_for("viewsCustomer.dashboard", c_id=int(user.customer_id))
                    )
                elif role == "admin":
                    session["account_type"] = "Admin"
                    return redirect(
                        url_for("viewsAdmin.dashboard", admin_id=int(user.admin_id))
                    )
                elif role == "store-manager":
                    session["account_type"] = "StoreManager"
                    return redirect(
                        url_for(
                            "viewsStoreMng.dashboard",
                            strmng_id=int(user.store_manager_id),
                        )
                    )
                elif role == "delivery-executive":
                    session["account_type"] = "DeliveryExecutive"
                    return redirect(
                        url_for(
                            "viewsDelExe.dashboard",
                            delexe_id=int(user.delivery_executive_id),
                        )
                    )
                elif role == "developer":
                    session["account_type"] = "developer"
                    access_token = create_access_token(identity=user.username)
                    Developer.query.filter_by(username=username).update(
                        dict(APIkey=access_token)
                    )
                    db.session.commit()
                    return redirect(
                        url_for(
                            "viewsDeveloper.dashboard", dev_id=int(user.developer_id)
                        )
                    )
                else:
                    flash("Can't get the correct role. Report admin.", category="error")
            else:
                flash("Incorrect password, try again.", category="error")
        else:
            flash("Username does not exist.", category="error")

    return render_template("signinup/signin_base.html")


# Signout route


@auth.route("/signout")
@login_required
def logout():
    logout_user()
    session.clear()
    response = redirect(url_for("auth.signin"))
    response.delete_cookie("remember_token")
    return response


# Signup routes


@auth.route("/customer_signup", methods=["GET", "POST"])
def customer_signup():
    if request.method == "POST":
        name = request.form.get("name")
        username = request.form.get("username")
        password = request.form.get("password")
        phone = request.form.get("phone")
        email = request.form.get("email")
        address = request.form.get("address")

        validate_features = check_user_features(
            Customer, name, username, phone, password, email
        )
        validate_address = check_address(address)
        if validate_features != True:
            flash(validate_features, category="error")
        elif validate_address != True:
            flash(validate_address, category="error")
        else:
            new = Customer(
                email=email,
                name=name,
                password=generate_password_hash(password),
                username=username,
                phone_no=phone,
                address=address,
            )
            db.session.add(new)
            db.session.commit()
            flash("Account created!", category="success")
            return redirect("/")
    return render_template("signinup/signup_customer.html")


@auth.route("/store_manager_signup", methods=["GET", "POST"])
def store_manager_signup():
    if request.method == "POST":
        name = request.form.get("name")
        username = request.form.get("username")
        password = request.form.get("password")
        phone = request.form.get("phone")
        email = request.form.get("email")
        strmng_id = request.form.get("store-manager-id")
        branch_id = request.form.get("branch-id")

        validate_features = check_user_features(
            StoreManager, name, username, phone, password, email
        )
        validate_strmng_ids = check_strmng_ids(int(strmng_id), int(branch_id))
        if validate_features != True:
            flash(validate_features, category="error")
        elif validate_strmng_ids != True:
            flash(validate_strmng_ids, category="error")
        else:
            new = StoreManager(
                store_manager_id=int(strmng_id),
                branch_id=int(branch_id),
                email=email,
                name=name,
                password=generate_password_hash(password),
                username=username,
                phone_no=phone,
            )
            db.session.add(new)
            db.session.commit()
            flash("Account created!", category="success")
            return redirect("/")
    return render_template("signinup/signup_storemng.html")


@auth.route("/delivery_executive_signup", methods=["GET", "POST"])
def delivery_executive_signup():
    if request.method == "POST":
        name = request.form.get("name")
        username = request.form.get("username")
        password = request.form.get("password")
        phone = request.form.get("phone")
        email = request.form.get("email")
        delexe_id = request.form.get("delivery-executive-id")
        branch_id = request.form.get("branch-id")

        validate_features = check_user_features(
            DeliveryExecutive, name, username, phone, password, email
        )
        validate_delexe_ids = check_delexe_ids(int(delexe_id), int(branch_id))
        if validate_features != True:
            flash(validate_features, category="error")
        elif validate_delexe_ids != True:
            flash(validate_delexe_ids, category="error")
        else:
            new = DeliveryExecutive(
                delivery_executive_id=int(delexe_id),
                branch_id=int(branch_id),
                email=email,
                name=name,
                password=generate_password_hash(password),
                username=username,
                phone_no=phone,
            )
            db.session.add(new)
            db.session.commit()
            flash("Account created!", category="success")
            return redirect("/")
    return render_template("signinup/signup_delexe.html")


@auth.route("/developer_signup", methods=["GET", "POST"])
def developer_signup():
    if request.method == "POST":
        name = request.form.get("name")
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        phone = "1234567890"
        validate_features = check_user_features(
            Developer, name, username, phone, password, email
        )
        if validate_features != True:
            flash(validate_features, category="error")
        else:
            new = Developer(
                email=email,
                name=name,
                password=generate_password_hash(password),
                username=username,
            )
            db.session.add(new)
            db.session.commit()
            flash("Account created!", category="success")
            return redirect("/")
    return render_template("signinup/signup_developer.html")


# Validation functions for sign up


def check_user_features(dbClass, name, username, phone, password, email):
    if dbClass.query.filter_by(username=username).first():
        return "Username already exists"
    elif dbClass.query.filter_by(phone_no=phone).first():
        return "Phone number already exists"
    elif len(username) < 8:
        return "Username must have atleast 8 characters"
    elif dbClass.query.filter_by(email=email).first():
        return "Email already exists"
    elif type(email) != str:
        return "Email must be a string"
    elif len(password) < 8:
        return "Password must have atleast 8 characters"
    elif len(phone) != 10 and phone.isdigit():
        return "Phone number must have 10 digits"
    elif type(name) != str:
        return "Name must be a string"
    else:
        return True


def check_address(address):
    if type(address) != str:
        return "Address must be a string"
    elif len(address) < 10:
        return "Address must have atleast 10 characters"
    else:
        return True


def check_strmng_ids(strmng_id, branch_id):
    strmng_entry = StoreManagerids.query.filter_by(
        store_manager_id=strmng_id, branch_id=branch_id
    ).first()
    strmng = StoreManager.query.filter_by(store_manager_id=strmng_id).first()
    if strmng:
        return "Store Manager ID already exists"
    elif strmng_entry:
        return True
    elif not StoreManagerids.query.filter_by(store_manager_id=strmng_id).first():
        return "Enter correct Store Manager ID"
    elif not StoreManagerids.query.filter_by(branch_id=branch_id).first():
        return "Enter correct Branch ID"
    else:
        return "Something went wrong! Contact Admin."


def check_delexe_ids(delexe_id, branch_id):
    delexe_entry = DeliveryExecutiveids.query.filter_by(
        delivery_executive_id=delexe_id, branch_id=branch_id
    ).first()
    delexe = DeliveryExecutive.query.filter_by(delivery_executive_id=delexe_id).first()
    if delexe:
        return "Delivery Executive ID already exists"
    elif delexe_entry:
        return True
    elif not DeliveryExecutiveids.query.filter_by(
        delivery_executive_id=delexe_id
    ).first():
        return "Enter correct Delivery Executive ID"
    elif not DeliveryExecutiveids.query.filter_by(branch_id=branch_id).first():
        return "Enter correct Branch ID"
    else:
        return "Something went wrong! Contact Admin."


# forgot password routes


@auth.route("/customer_forgot_password", methods=["GET", "POST"])
def customer_forgot_password():
    if request.method == "POST":
        flag = request.form.get("flag")
        id = request.form.get("id")
        if flag == "True":
            username = request.form.get("username")
            email = request.form.get("email")
            phone_no = request.form.get("phone_no")
            user = Customer.query.filter_by(username=username).first()
            if user:
                if user.email == email and user.phone_no == phone_no:
                    otp = generateOTP()
                    session["otp"] = otp
                    sendOTP(otp, phone_no)
                    return render_template(
                        "signinup/forgot_pswd.html", flag=False, id=user.customer_id
                    )
                else:
                    flash(
                        "Email and phone number doesnot match username",
                        category="error",
                    )
                    return render_template(
                        "signinup/forgot_pswd.html", flag=True, id=None
                    )
            else:
                flash("Invalid credentials", category="error")
                return render_template("signinup/forgot_pswd.html", flag=True, id=None)
        else:
            otp = request.form.get("otp")
            saved_otp = session.get("otp")
            id = request.form.get("id")
            if str(otp) == str(saved_otp):
                return redirect(url_for("auth.customer_reset_password", c_id=id))
            else:
                flash("Invalid OTP", category="error")
                return render_template("signinup/forgot_pswd.html", flag=True, id=None)
    return render_template("signinup/forgot_pswd.html", flag=True, id=None)


@auth.route("/customer_reset_password/<int:c_id>", methods=["GET", "POST"])
def customer_reset_password(c_id):
    if request.method == "POST":
        new_pswd = request.form.get("new_pswd")
        if len(new_pswd) < 8:
            flash("Password must have atleast 8 characters", category="error")
            return render_template("signinup/set_new_pswd.html", id=c_id)
        else:
            user = Customer.query.filter_by(customer_id=c_id).first()
            user.password = generate_password_hash(new_pswd)
            db.session.commit()
            flash("Password changed successfully", category="success")
            return redirect("/")
    return render_template("signinup/set_new_pswd.html", id=c_id)


# No forgot password and reset password routes for admin :
# it wouldn't make much sense since admin only have username and password
# but there should be some provision to update the passsword(outside the control of the developer) for security purposes
# maybe admin can have a phone no to update the password?


@auth.route("/store_manager_forgot_password", methods=["GET", "POST"])
def store_manager_forgot_password():
    if request.method == "POST":
        flag = request.form.get("flag")
        id = request.form.get("id")
        if flag == "True":
            username = request.form.get("username")
            email = request.form.get("email")
            phone_no = request.form.get("phone_no")
            user = StoreManager.query.filter_by(username=username).first()
            if user:
                if user.email == email and user.phone_no == phone_no:
                    otp = generateOTP()
                    session["otp"] = otp
                    sendOTP(otp, phone_no)
                    return render_template(
                        "signinup/forgot_pswd.html",
                        flag=False,
                        id=user.store_manager_id,
                    )
                else:
                    flash(
                        "Email and phone number doesnot match username",
                        category="error",
                    )
                    return render_template(
                        "signinup/forgot_pswd.html", flag=True, id=None
                    )
            else:
                flash("Invalid credentials", category="error")
                return render_template("signinup/forgot_pswd.html", flag=True, id=None)
        else:
            otp = request.form.get("otp")
            saved_otp = session.get("otp")
            id = request.form.get("id")
            if str(otp) == str(saved_otp):
                return redirect(
                    url_for("auth.store_manager_reset_password", strmng_id=id)
                )
            else:
                flash("Invalid OTP", category="error")
                return render_template("signinup/forgot_pswd.html", flag=True, id=None)
    return render_template("signinup/forgot_pswd.html", flag=True, id=None)


@auth.route("/store_manager_reset_password/<int:strmng_id>", methods=["GET", "POST"])
def store_manager_reset_password(strmng_id):
    if request.method == "POST":
        new_pswd = request.form.get("new_pswd")
        if len(new_pswd) < 8:
            flash("Password must have atleast 8 characters", category="error")
            return render_template("signinup/set_new_pswd.html", id=strmng_id)
        else:
            user = StoreManager.query.filter_by(store_manager_id=strmng_id).first()
            user.password = generate_password_hash(new_pswd)
            db.session.commit()
            flash("Password changed successfully", category="success")
            return redirect("/")
    return render_template("signinup/set_new_pswd.html", id=strmng_id)


@auth.route("/delivery_executive_forgot_password", methods=["GET", "POST"])
def delivery_executive_forgot_password():
    if request.method == "POST":
        flag = request.form.get("flag")
        id = request.form.get("id")
        if flag == "True":
            username = request.form.get("username")
            email = request.form.get("email")
            phone_no = request.form.get("phone_no")
            user = DeliveryExecutive.query.filter_by(username=username).first()
            if user:
                if user.email == email and user.phone_no == phone_no:
                    otp = generateOTP()
                    session["otp"] = otp
                    sendOTP(otp, phone_no)
                    return render_template(
                        "signinup/forgot_pswd.html",
                        flag=False,
                        id=user.delivery_executive_id,
                    )
                else:
                    flash(
                        "Email and phone number doesnot match username",
                        category="error",
                    )
                    return render_template(
                        "signinup/forgot_pswd.html", flag=True, id=None
                    )
            else:
                flash("Invalid credentials", category="error")
                return render_template("signinup/forgot_pswd.html", flag=True, id=None)
        else:
            otp = request.form.get("otp")
            saved_otp = session.get("otp")
            id = request.form.get("id")
            if str(otp) == str(saved_otp):
                return redirect(
                    url_for("auth.delivery_executive_reset_password", delexe_id=id)
                )
            else:
                flash("Invalid OTP", category="error")
                return render_template("signinup/forgot_pswd.html", flag=True, id=None)
    return render_template("signinup/forgot_pswd.html", flag=True, id=None)


@auth.route(
    "/delivery_executive_reset_password/<int:delexe_id>", methods=["GET", "POST"]
)
def delivery_executive_reset_password(delexe_id):
    if request.method == "POST":
        new_pswd = request.form.get("new_pswd")
        if len(new_pswd) < 8:
            flash("Password must have atleast 8 characters", category="error")
            return render_template("signinup/set_new_pswd.html", id=delexe_id)
        else:
            user = DeliveryExecutive.query.filter_by(
                delivery_executive_id=delexe_id
            ).first()
            user.password = generate_password_hash(new_pswd)
            db.session.commit()
            flash("Password changed successfully", category="success")
            return redirect("/")
    return render_template("signinup/set_new_pswd.html", id=delexe_id)


@auth.route("/developer_forgot_password", methods=["GET", "POST"])
def developer_forgot_password():
    return "still in development"
