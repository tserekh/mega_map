from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

from config import SQLALCHEMY_DATABASE_URI

application = Flask(__name__)
application.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
con = create_engine(application.config["SQLALCHEMY_DATABASE_URI"])

db = SQLAlchemy(application)
migrate = Migrate(application, db)
