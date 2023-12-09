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


@viewsAdmin.route("/admin/<int:admin_id>/dashboard")
def dashboard(admin_id):
    return render_template("dashboard/dashboard_admin.html", admin_id=admin_id)
