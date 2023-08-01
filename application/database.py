
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import current_app as app

engine=None
Base=declarative_base()
db=SQLAlchemy()
migrate = Migrate(app, db)

