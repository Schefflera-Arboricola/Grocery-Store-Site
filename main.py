import os
from flask_login import LoginManager, UserMixin
from flask import Flask,session
from flask_restful import Resource,Api
from flask_cors import CORS  #cross origin and resource sharing
from application import config
from application.config import LocalDevelopmentConfig
from application.database import db
from flask_sqlalchemy import SQLAlchemy


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    CORS(app)
    if os.getenv('ENV',"development")=="production": 
        raise Exception("Currently no production config is setup.")
    else:
        print("Starting Local Development")
        app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    app.app_context().push()
    #from application.views import views
    from application.auth import auth

    #app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    api=Api(app)
   

    from application.models import Customer,StoreManager,DeliveryExecutive

    login_manager = LoginManager()
    login_manager.login_view = 'auth.signin'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # Determine the user type based on the prefix in the user_id
        if session['account_type'] == 'Customer':
            return Customer.query.get(int(user_id))
        elif session['account_type'] == 'StoreManager':
            return StoreManager.query.get(int(user_id))
        elif session['account_type'] == 'DeliveryExecutive':
            return DeliveryExecutive.query.get(int(user_id))
        else:
            return None
        
    return app,api

app,api=create_app()

if __name__=='__main__':
    app.run(host='0.0.0.0',debug=True,port=8080)



'''
def create_app():
    app=Flask(__name__)
    app.secret_key = 'your_secret_key'
    CORS(app)
    if os.getenv('ENV',"development")=="production": 
        raise Exception("Currently no production config is setup.")
    else:
        print("Starting Local Development")
        app.config.from_object(LocalDevelopmentConfig)
    #api.init_app(app)
    db.init_app(app)
    api=Api(app)
    app.app_context().push()
    return app,api


app,api=create_app()
from application.controllers import *
#from application.api import UserAPI

#api.add_resource(UserAPI,'/api/user','/api/user/<string:username>')

'''
