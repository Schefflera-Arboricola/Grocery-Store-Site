import os
from flask import Flask
from flask_cors import CORS  #cross origin and resource sharing
from application import config
from application.config import LocalDevelopmentConfig
from application.database import db
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
import stripe

def create_app():
    app = Flask(__name__)
    app.config['PERMANENT_SESSION_LIFETIME'] = 3600 # 1 hour : session time(for OTPs)
    app.config['SECRET_KEY'] = 'asdfghjklzxcvbnm'
    app.secret_key = 'qwertyuiopasdfghjkl'
    
    app.config['STRIPE_PUBLIC_KEY']=''
    app.config['STRIPE_SECRET_KEY']=''

    CORS(app)
    if os.getenv('ENV',"development")=="production": 
        raise Exception("Currently no production config is setup.")
    else:
        print("Starting Local Development")
        app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    app.app_context().push()

    from application.views.viewsCustomer import viewsCustomer
    from application.views.viewsDelExe import viewsDelExe 
    from application.views.viewsStoreMng import viewsStoreMng
    from application.views.auth import auth

    app.register_blueprint(viewsCustomer, url_prefix='/')
    app.register_blueprint(viewsDelExe, url_prefix='/')
    app.register_blueprint(viewsStoreMng, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')


    from application.api import CategoryAPI, ProductAPI

    api=Api(app)
    api.init_app(app)

    api.add_resource(CategoryAPI, '/categories', '/categories/<int:category_id>')
    api.add_resource(ProductAPI, '/products', '/products/<int:product_id>', '/products/<int:flag>/<int:category_id>/') #flag tells if the entered id is category_id or product_id

    return app,api

app,api=create_app()


if __name__=='__main__':
    app.run(host='0.0.0.0',debug=True,port=8080)