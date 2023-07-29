import os
from twilio.rest import Client
from flask import current_app as app
import stripe
from flask_jwt_extended import JWTManager

account_sid = ''
auth_token = '' 
sender_phone = ''
client = Client(account_sid, auth_token)

app.config['STRIPE_PUBLIC_KEY']=''
app.config['STRIPE_SECRET_KEY']=''

app.config['PERMANENT_SESSION_LIFETIME'] = 3600 # 1 hour : session time(for OTPs)
app.config['SECRET_KEY'] = 'secret_key'

basedir=os.path.abspath(os.path.dirname(__file__))

app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'your-secret-key')
jwt = JWTManager(app)

class Config():
    DEBUG=False
    SQLITE_DB_DIR=None
    SQLALCHEMY_DATABASE_URI=None
    SQLALCHEMY_TRACK_MODIFICATIONS=False

class LocalDevelopmentConfig(Config):
    SQLITE_DB_DIR=os.path.join(basedir,"../db_directory")
    SQLALCHEMY_DATABASE_URI='sqlite:///'+os.path.join(SQLITE_DB_DIR,"gs.sqlite3")
    DEBUG=True

class ProductionDevelopmentConfig(Config):
    SQLITE_DB_DIR=os.path.join(basedir,"../db_directory")
    SQLALCHEMY_DATABASE_URI='sqlite:///'+os.path.join(SQLITE_DB_DIR,"gs.sqlite3")
    DEBUG=False
