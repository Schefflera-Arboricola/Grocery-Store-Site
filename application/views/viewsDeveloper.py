from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_required, current_user
from flask import current_app as app
from application.models import *
from application.database import db

viewsDeveloper = Blueprint("viewsDeveloper", __name__)


@viewsDeveloper.before_request
@login_required
def require_login():
    developer_id = request.view_args.get("dev_id")
    if (
        not isinstance(current_user, Developer)
        or current_user.developer_id != developer_id
    ):
        return render_template("error.html"), 401


@viewsDeveloper.route("/developer/<int:dev_id>/dashboard")
def dashboard(dev_id):
    user = Developer.query.filter_by(developer_id=dev_id).first()
    content = read_apidoc_content()
    return render_template(
        "dashboard/dashboard_developer.html",
        id=dev_id,
        name=user.name,
        username=user.username,
        email=user.email,
        account_type="developer",
        swagger_content=content,
    )


def read_apidoc_content():
    with open("application/APIdoc.yaml", "r") as file:
        content = file.read()
    return content


@viewsDeveloper.route("/developer/<int:dev_id>/editProfile", methods=["GET", "POST"])
def editProfile(dev_id):
    return "still in development"


@viewsDeveloper.route("/developer/<int:dev_id>/getAPI", methods=["GET", "POST"])
def getAPI(dev_id):
    user = Developer.query.filter_by(developer_id=dev_id).first()
    APIkey = user.APIkey
    return render_template(
        "userviews/developer/getAPIcredentials.html", dev_id=dev_id, APIkey=APIkey
    )
