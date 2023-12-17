from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify
from flask_login import login_required, current_user
from flask import current_app as app
from application.models import *
from application.database import db
from werkzeug.security import check_password_hash
from werkzeug.datastructures import ImmutableMultiDict
from db_directory.accessDB import *
import pandas as pd
from application.config import cache

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
    elif current_user.isApproved == "Pending":
        return render_template("userviews/store_manager/pending.html"), 403


@viewsStoreMng.route("/storemng/<int:strmng_id>/dashboard")
@cache.cached(timeout=20)
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

@viewsStoreMng.route('/storemng/<int:strmng_id>/export-products', methods=['POST'])
def trigger_export_products(strmng_id):
    if request.method == 'POST':
        try:
            products = Products.query.all()
            columns = Products.__table__.columns.keys()
            data = [{column: getattr(product, column) for column in columns} for product in products]

            print(data)
            df = pd.DataFrame(data)
            csv_filename = "all_products.csv"
            df.to_csv(csv_filename, index=False)

            return jsonify(message='Exporting products task completed successfully.', status='success')
        except Exception as e:
            return jsonify(message='Error exporting products: {}'.format(str(e)), status='error')


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


@viewsStoreMng.route("/storemng/<int:strmng_id>/pastRequests")
def pastRequests(strmng_id):
    past_requests = CategoryUpdateRequest.query.filter(
        CategoryUpdateRequest.isApproved.in_(["Approved", "Rejected"])
    ).all()
    past_requests = [
        update for update in past_requests if update.store_manager_id == strmng_id
    ]
    return render_template(
        "userviews/store_manager/pastRequests.html",
        strmng_id=strmng_id,
        past_requests=past_requests,
    )


@viewsStoreMng.route("/storemng/<int:strmng_id>/pendingRequests")
def pendingRequests(strmng_id):
    pending_requests = CategoryUpdateRequest.query.filter_by(
        isApproved="No Action"
    ).all()
    pending_requests = [
        update for update in pending_requests if update.store_manager_id == strmng_id
    ]
    return render_template(
        "userviews/store_manager/pendingRequests.html",
        strmng_id=strmng_id,
        pending_requests=pending_requests,
    )


@viewsStoreMng.route(
    "/storemng/<int:strmng_id>/requestDetails/<int:update_id>", methods=["GET", "POST"]
)
def requestDetails(strmng_id, update_id):
    update = CategoryUpdateRequest.query.filter_by(update_id=update_id).first()
    if update.category_id:
        category = Category.query.filter_by(category_id=update.category_id).first()
    return render_template(
        "userviews/store_manager/requestDetails.html",
        strmng_id=strmng_id,
        update=update,
        category=category,
    )


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


@viewsStoreMng.route("/storemng/<int:strmng_id>/createRequest", methods=["GET", "POST"])
def createRequest(strmng_id):
    categories = Category.query.all()
    if request.method == "POST":
        request_info = request.form
        update_type = request_info["update_type"]
        if request_info["update_type"] in ["UPDATE", "DELETE"]:
            category_id = request_info["category_id"]
        elif request_info["update_type"] == "ADD":
            category_id = None
        new_update = CategoryUpdateRequest(
            store_manager_id=strmng_id,
            category_id=category_id,
            update_type=update_type,
            update_heading=request_info["update_heading"],
            update_description1=request_info["update_description1"],
            update_description2=request_info["update_description2"],
        )
        db.session.add(new_update)
        db.session.commit()
        return redirect(url_for("viewsStoreMng.pendingRequests", strmng_id=strmng_id))
    return render_template(
        "userviews/store_manager/createRequest.html", categories=categories
    )
