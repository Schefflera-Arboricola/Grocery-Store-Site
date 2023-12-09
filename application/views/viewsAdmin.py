from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from application.models import *
from db_directory.accessDB import *

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
    return render_template("dashboard/dashboard_admin.html", admin_id=admin_id, pending=pending_sm)

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