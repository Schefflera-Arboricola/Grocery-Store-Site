from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_required, current_user
from flask import current_app as app
from application.models import *
from application.database import db
from werkzeug.security import check_password_hash
from werkzeug.datastructures import ImmutableMultiDict
from db_directory.accessDB import *

viewsStoreMng = Blueprint("viewsStoreMng", __name__)


@viewsStoreMng.before_request
@login_required
def require_login():
    store_manager_id = request.view_args.get("strmng_id")
    if (
        not isinstance(current_user, StoreManager)
        or current_user.store_manager_id != store_manager_id
    ):
        return render_template("error.html"), 401
    elif current_user.isApproved == "Pending" :
        return render_template("userviews/store_manager/pending.html"), 403
    # elif current_user.isApproved == "Rejected" :
        # return render_template("userviews/store_manager/rejected.html"), 403
    else :
        return "Error!! Please contact the developer.", 404

@viewsStoreMng.route("/storemng/<int:strmng_id>/dashboard")
def dashboard(strmng_id):
    user = StoreManager.query.filter_by(store_manager_id=strmng_id).first()
    return render_template(
        "dashboard/dashboard_storemng.html",
        id=strmng_id,
        name=user.name,
        phone=user.phone_no,
        username=user.username,
        email=user.email,
        account_type="storemng",
    )


@viewsStoreMng.route("/storemng/<int:strmng_id>/editProfile", methods=["GET", "POST"])
def editProfile(strmng_id):
    if request.method == "POST":
        name = request.form.get("name")
        phone = request.form.get("phone")
        password = request.form.get("password")
        user = StoreManager.query.filter_by(store_manager_id=strmng_id).first()
        user.name = name
        user.phone_no = phone
        if check_password_hash(user.password, password):
            features = check_user_features(name, phone)
            if features != True:
                flash(features, category="error")
                return render_template(
                    "editProfile/editProfile_storemng.html",
                    name=user.name,
                    phone=user.phone_no,
                )
            else:
                db.session.commit()
                return redirect(url_for("viewsStoreMng.dashboard", strmng_id=strmng_id))
        else:
            flash("Incorrect password, try again.", category="error")
            return render_template(
                "editProfile/editProfile_storemng.html",
                name=user.name,
                phone=user.phone_no,
            )
    else:
        user = StoreManager.query.filter_by(store_manager_id=strmng_id).first()
        return render_template(
            "editProfile/editProfile_storemng.html", name=user.name, phone=user.phone_no
        )


def check_user_features(name, phone):
    if len(phone) != 10 and phone.isdigit():
        return "Phone number must have 10 digits"
    elif type(name) != str:
        return "Name must be a string"
    else:
        return True


# Product Management


@viewsStoreMng.route("/storemng/<int:strmng_id>/Product", methods=["GET", "POST"])
def Product(strmng_id):
    products, status_code = GetProduct()
    return render_template(
        "userviews/store_manager/viewProducts.html",
        products=products,
        strmng_id=strmng_id,
    )


@viewsStoreMng.route("/storemng/<int:strmng_id>/addProduct", methods=["GET", "POST"])
def addProduct(strmng_id):
    if request.method == "POST":
        product_info = request.form
        products, status_code = AddProduct(product_info)
        if status_code == 404:
            flash(products["message"], category="error")
        elif status_code == 200:
            return redirect(url_for("viewsStoreMng.Product", strmng_id=strmng_id))
        else:
            flash("Something went wrong. Contact Admin", category="error")
    return render_template("userviews/store_manager/addProduct.html")


@viewsStoreMng.route(
    "/storemng/<int:strmng_id>/editProduct/<int:prod_id>", methods=["GET", "POST"]
)
def editProduct(strmng_id, prod_id):
    if request.method == "POST":
        product_info = request.form
        product_info = product_info.to_dict()
        product, status_code = GetProduct(prod_id)
        product_info["avg_rating"] = product["avg_rating"]
        products, status_code = UpdateProduct(prod_id, ImmutableMultiDict(product_info))
        if status_code == 404:
            flash(products["message"], category="error")
        elif status_code == 200:
            return redirect(url_for("viewsStoreMng.Product", strmng_id=strmng_id))
        else:
            flash("Something went wrong. Contact Admin", category="error")
    product = Products.query.filter_by(product_id=prod_id).first()
    return render_template("userviews/store_manager/editProduct.html", product=product)


@viewsStoreMng.route(
    "/storemng/<int:strmng_id>/deleteProduct/<int:prod_id>", methods=["GET", "POST"]
)
def deleteProduct(strmng_id, prod_id):
    products, status_code = DeleteProduct(prod_id)
    if status_code == 404:
        print(products["message"])
    elif status_code == 200:
        return redirect(url_for("viewsStoreMng.Product", strmng_id=strmng_id))
    else:
        print("Something went wrong. Contact Admin")
    return redirect(url_for("viewsStoreMng.Product", strmng_id=strmng_id))


# Category Management


@viewsStoreMng.route("/storemng/<int:strmng_id>/Category", methods=["GET", "POST"])
def Categories(strmng_id):
    categories, status_code = GetCategory()
    return render_template(
        "userviews/store_manager/viewCategories.html",
        categories=categories,
        strmng_id=strmng_id,
    )


@viewsStoreMng.route("/storemng/<int:strmng_id>/addCategory", methods=["GET", "POST"])
def addCategory(strmng_id):
    if request.method == "POST":
        categories, status_code = AddCategory(request.form)
        if status_code == 404:
            flash(categories["message"], category="error")
        elif status_code == 200:
            return redirect(url_for("viewsStoreMng.Categories", strmng_id=strmng_id))
        else:
            flash("Something went wrong. Contact Admin", category="error")
    return render_template("userviews/store_manager/addCategory.html")


@viewsStoreMng.route(
    "/storemng/<int:strmng_id>/editCategory/<int:cat_id>", methods=["GET", "POST"]
)
def editCategory(strmng_id, cat_id):
    if cat_id != 0:
        category = Category.query.filter_by(category_id=cat_id).first()
        if request.method == "POST":
            categories, status_code = UpdateCategory(cat_id, request.form)
            if status_code == 404:
                flash(categories["message"], category="error")
            elif status_code == 200:
                return redirect(
                    url_for("viewsStoreMng.Categories", strmng_id=strmng_id)
                )
            else:
                flash("Something went wrong. Contact Admin", category="error")
        return render_template(
            "userviews/store_manager/editCategory.html", category=category
        )
    else:
        return render_template("error.html")


@viewsStoreMng.route(
    "/storemng/<int:strmng_id>/deleteCategory/<int:cat_id>", methods=["GET", "POST"]
)
def deleteCategory(strmng_id, cat_id):
    if cat_id != 0:
        categories, status_code = DeleteCategory(cat_id)
        if status_code == 404:
            print(categories["message"])
        elif status_code == 200:
            return redirect(url_for("viewsStoreMng.Categories", strmng_id=strmng_id))
        else:
            print("Something went wrong. Contact Admin")
        return redirect(url_for("viewsStoreMng.Categories", strmng_id=strmng_id))
    else:
        return render_template("error.html")
