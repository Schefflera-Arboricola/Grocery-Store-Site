import os
from flask import Flask
from flask_restful import Resource,Api
from flask_cors import CORS  #cross origin and resource sharing
from application import config
from application.config import LocalDevelopmentConfig
from application.database import db

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

if __name__=='__main__':
    app.run(host='0.0.0.0',debug=True,port=8080)

