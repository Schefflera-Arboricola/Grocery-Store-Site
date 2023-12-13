from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_required, current_user
from application.models import *
from db_directory.accessDB import *
from werkzeug.datastructures import ImmutableMultiDict

viewsAdmin = Blueprint("viewsAdmin", __name__)


@viewsAdmin.before_request
@login_required
def require_login():
    admin_id = request.view_args.get("admin_id")
    if (
        not isinstance(current_user, Admin)
        or current_user.admin_id != admin_id
        or admin_id != 1
    ):
        return render_template("error.html"), 401


@viewsAdmin.route("/admin/<int:admin_id>/dashboard", methods=["GET", "POST"])
def dashboard(admin_id):
    if request.method == "POST":
        for key, value in request.form.items():
            if key.startswith("status_"):
                store_manager_id = int(key.replace("status_", ""))
                update_status_in_database(store_manager_id, value)

    pending_sm = StoreManager.query.filter_by(isApproved="Pending").all()
    return render_template(
        "dashboard/dashboard_admin.html", admin_id=admin_id, pending=pending_sm
    )


def update_status_in_database(store_manager_id, new_status):
    store_manager = StoreManager.query.get(store_manager_id)
    if store_manager:
        if new_status == "Approved":
            store_manager.isApproved = "Approved"
        elif new_status == "Pending":
            store_manager.isApproved = "Pending"
        elif new_status == "Rejected":
            db.session.delete(store_manager)
            # todo : notify that their signup has been rejected
        db.session.commit()


@viewsAdmin.route("/admin/<int:admin_id>/updateHistory")
def updateHistory(admin_id):
    past_updates = CategoryUpdateRequest.query.filter(
        CategoryUpdateRequest.isApproved.in_(["Approved", "Rejected"])
    ).all()
    return render_template(
        "userviews/admin/updateHistory.html",
        admin_id=admin_id,
        past_updates=past_updates,
    )


@viewsAdmin.route("/admin/<int:admin_id>/categoryUpdateRequests")
def categoryUpdateRequests(admin_id):
    pending_updates = CategoryUpdateRequest.query.filter_by(
        isApproved="No Action"
    ).all()
    return render_template(
        "userviews/admin/categoryUpdateRequests.html",
        admin_id=admin_id,
        pending_updates=pending_updates,
    )


@viewsAdmin.route(
    "/admin/<int:admin_id>/updateDetails/<int:update_id>", methods=["GET", "POST"]
)
def updateDetails(admin_id, update_id):
    update = CategoryUpdateRequest.query.filter_by(update_id=update_id).first()
    store_manager_details = StoreManager.query.filter_by(
        store_manager_id=update.store_manager_id
    ).first()
    if update.category_id:
        category = Category.query.filter_by(category_id=update.category_id).first()
    else:
        category = None
    if request.method == "POST":
        if request.form.get("status") == "Approved":
            update.isApproved = "Approved"
            if update.update_type == "ADD":
                data = {
                    "name": update.update_description1,
                    "description": update.update_description2,
                }
                msg, status_code = AddCategory(data)
                if status_code == 200:
                    new_category = Category.query.order_by(
                        Category.category_id.desc()
                    ).first()
                    update.category_id = new_category.category_id
                    db.session.commit()
                    update.feedback = request.form.get("feedback")
                    db.session.commit()
            elif update.update_type == "DELETE":
                msg, status_code = DeleteCategory(update.category_id)
                if status_code == 200:
                    update.feedback = request.form.get("feedback")
                    db.session.commit()
            elif update.update_type == "UPDATE":
                data = {
                    "name": update.update_description1,
                    "description": update.update_description2,
                }
                msg, status_code = UpdateCategory(update.category_id, data)
                if status_code == 200:
                    update.feedback = request.form.get("feedback")
                    db.session.commit()
            return render_template(
                "userviews/admin/mergeResult.html",
                admin_id=admin_id,
                status_code=status_code,
                msg=msg["message"],
            )
        elif request.form.get("status") == "Rejected":
            update.isApproved = "Rejected"
            db.session.commit()
            update.feedback = request.form.get("feedback")
            db.session.commit()
            return redirect(
                url_for("viewsAdmin.categoryUpdateRequests", admin_id=admin_id)
            )
    return render_template(
        "userviews/admin/updateDetailsPage.html",
        admin_id=admin_id,
        update=update,
        category=category,
        store_manager=store_manager_details,
    )


# Category Management


@viewsAdmin.route("/admin/<int:admin_id>/Category", methods=["GET", "POST"])
def Categories(admin_id):
    categories, status_code = GetCategory()
    return render_template(
        "userviews/admin/viewCategories.html", categories=categories, admin_id=admin_id,
    )


@viewsAdmin.route("/admin/<int:admin_id>/addCategory", methods=["GET", "POST"])
def addCategory(admin_id):
    if request.method == "POST":
        categories, status_code = AddCategory(request.form)
        if status_code == 404:
            flash(categories["message"], category="error")
        elif status_code == 200:
            return redirect(url_for("viewsAdmin.Categories", admin_id=admin_id))
        else:
            flash("Something went wrong. Contact Developer", category="error")
    return render_template("userviews/admin/addCategory.html")


@viewsAdmin.route(
    "/admin/<int:admin_id>/editCategory/<int:cat_id>", methods=["GET", "POST"]
)
def editCategory(admin_id, cat_id):
    if cat_id != 0:
        category = Category.query.filter_by(category_id=cat_id).first()
        if request.method == "POST":
            categories, status_code = UpdateCategory(cat_id, request.form)
            if status_code == 404:
                flash(categories["message"], category="error")
            elif status_code == 200:
                return redirect(url_for("viewsAdmin.Categories", admin_id=admin_id))
            else:
                flash("Something went wrong. Contact Developer", category="error")
        return render_template("userviews/admin/editCategory.html", category=category)
    else:
        return render_template("error.html")


@viewsAdmin.route(
    "/admin/<int:admin_id>/deleteCategory/<int:cat_id>", methods=["GET", "POST"]
)
def deleteCategory(admin_id, cat_id):
    if cat_id != 0:
        categories, status_code = DeleteCategory(cat_id)
        if status_code == 404:
            print(categories["message"])
        elif status_code == 200:
            return redirect(url_for("viewsAdmin.Categories", admin_id=admin_id))
        else:
            print("Something went wrong. Contact Developer")
        return redirect(url_for("viewsAdmin.Categories", admin_id=admin_id))
    else:
        return render_template("error.html")


# Product Management


@viewsAdmin.route("/admin/<int:admin_id>/Product", methods=["GET", "POST"])
def Product(admin_id):
    products, status_code = GetProduct()
    return render_template(
        "userviews/store_manager/viewProducts.html",
        products=products,
        strmng_id=admin_id,
    )


@viewsAdmin.route("/admin/<int:admin_id>/addProduct", methods=["GET", "POST"])
def addProduct(admin_id):
    if request.method == "POST":
        product_info = request.form
        products, status_code = AddProduct(product_info)
        if status_code == 404:
            flash(products["message"], category="error")
        elif status_code == 200:
            return redirect(url_for("viewsAdmin.Product", admin_id=admin_id))
        else:
            flash("Something went wrong. Contact Developer", category="error")
    return render_template("userviews/store_manager/addProduct.html")


@viewsAdmin.route(
    "/admin/<int:admin_id>/editProduct/<int:prod_id>", methods=["GET", "POST"]
)
def editProduct(admin_id, prod_id):
    if request.method == "POST":
        product_info = request.form
        product_info = product_info.to_dict()
        product, status_code = GetProduct(prod_id)
        product_info["avg_rating"] = product["avg_rating"]
        products, status_code = UpdateProduct(prod_id, ImmutableMultiDict(product_info))
        if status_code == 404:
            flash(products["message"], category="error")
        elif status_code == 200:
            return redirect(url_for("viewsAdmin.Product", admin_id=admin_id))
        else:
            flash("Something went wrong. Contact Developer", category="error")
    product = Products.query.filter_by(product_id=prod_id).first()
    return render_template("userviews/store_manager/editProduct.html", product=product)


@viewsAdmin.route(
    "/admin/<int:admin_id>/deleteProduct/<int:prod_id>", methods=["GET", "POST"]
)
def deleteProduct(admin_id, prod_id):
    products, status_code = DeleteProduct(prod_id)
    if status_code == 404:
        print(products["message"])
    elif status_code == 200:
        return redirect(url_for("viewsAdmin.Product", admin_id=admin_id))
    else:
        print("Something went wrong. Contact Developer")
    return redirect(url_for("viewsAdmin.Product", admin_id=admin_id))
