from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask import current_app as app
from application.models import *
from application.database import db

viewsCustomer = Blueprint('viewsCustomer', __name__)

@viewsCustomer.route('/customer/{customer_id}/dashboard')
def dashboard():
    return render_template("dashboard/dashboard_customer.html")