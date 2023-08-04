import os
from flask import Flask
from flask_restx import Api
from flask_cors import CORS

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

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    from flask import Blueprint
    from application.api import CategoryAPI, ProductAPI

    api_bp = Blueprint('api', __name__)
    api = Api(api_bp, version='1.0', title='API', description='API documentation')

    api.add_resource(CategoryAPI, '/categories', '/categories/<int:category_id>')
    api.add_resource(ProductAPI, '/products', '/products/<int:product_id>', '/products/<int:flag>/<int:category_id>')

    app.register_blueprint(api_bp, url_prefix='/api')

    return app,api

app,api=create_app()


if __name__=='__main__':
    app.run(host='0.0.0.0',debug=True,port=8080)