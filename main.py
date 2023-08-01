import os
from flask import Flask
from flask_restful import Api

def create_app():
    app = Flask(__name__)
    app.app_context().push()
    from application.config import LocalDevelopmentConfig
    
    if os.getenv('ENV',"development")=="production": 
        raise Exception("Currently no production config is setup.")
    else:
        print("Starting Local Development")
        app.config.from_object(LocalDevelopmentConfig)
    from application.database import db
    db.init_app(app)

    from application.views.viewsCustomer import viewsCustomer
    from application.views.viewsDelExe import viewsDelExe 
    from application.views.viewsStoreMng import viewsStoreMng
    from application.views.viewsDeveloper import viewsDeveloper
    from application.views.auth import auth

    app.register_blueprint(viewsCustomer, url_prefix='/')
    app.register_blueprint(viewsDelExe, url_prefix='/')
    app.register_blueprint(viewsStoreMng, url_prefix='/')
    app.register_blueprint(viewsDeveloper, url_prefix='/')
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