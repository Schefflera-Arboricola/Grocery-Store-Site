import os
from twilio.rest import Client
from flask import current_app as app
from flask_jwt_extended import JWTManager

account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
sender_phone = os.environ.get('TWILIO_SENDER_PHONE')

if not (account_sid and auth_token and sender_phone):
    raise Exception("Twilio API credentials are not provided. Please set TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, and TWILIO_SENDER_PHONE environment variables.")

client = Client(account_sid, auth_token)

stripe_public_key = os.environ.get('STRIPE_PUBLIC_KEY')
stripe_secret_key = os.environ.get('STRIPE_SECRET_KEY')

if not (stripe_public_key and stripe_secret_key):
    raise Exception("Stripe API keys are not provided. Please set STRIPE_PUBLIC_KEY and STRIPE_SECRET_KEY environment variables.")

app.config['STRIPE_PUBLIC_KEY'] = stripe_public_key
app.config['STRIPE_SECRET_KEY'] = stripe_secret_key

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
    #for docker 
    SQLITE_DB_DIR = "/app/db_directory" if os.getenv("ENV") == "development" else os.path.join(basedir, "../db_directory")
    
    #for virtual environment
    #SQLITE_DB_DIR=os.path.join(basedir,"../db_directory")

    SQLALCHEMY_DATABASE_URI='sqlite:///'+os.path.join(SQLITE_DB_DIR,"gs.sqlite3")
    DEBUG=True

class ProductionDevelopmentConfig(Config):
    SQLITE_DB_DIR=os.path.join(basedir,"../db_directory")
    SQLALCHEMY_DATABASE_URI='sqlite:///'+os.path.join(SQLITE_DB_DIR,"gs.sqlite3")
    DEBUG=False
