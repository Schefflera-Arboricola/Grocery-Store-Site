from flask import Blueprint, render_template, request, flash, redirect, url_for
from application.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from application.database import db   
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


