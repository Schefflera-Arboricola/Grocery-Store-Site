from twilio.rest import Client
account_sid = ''
auth_token = '' 
sender_phone = ''
client = Client(account_sid, auth_token)

import os
basedir=os.path.abspath(os.path.dirname(__file__))

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
