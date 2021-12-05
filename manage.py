import glob
import os
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from flask import Flask, flash, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from PIL import Image
from sqlalchemy import create_engine
import pandas as pd
from utils import get_clusters

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://postgres:postgres@postgres:5432/postgres"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.secret_key = 'secret string'
con = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])

db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))


class AbstractClass(db.Model):
    class Meta:
        abstract = True

    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Float())
    lon = db.Column(db.Float())

    x = db.Column(db.Float())
    y = db.Column(db.Float())

    address = db.Column(db.Text())
    source_id = db.Column(db.Text())
    source_name = db.Column(db.Text())
    info = db.Column(db.Text())


class MetroStation(AbstractClass):
    station_name = db.Column(db.Text())


class Metro(AbstractClass):
    # station_name = db.Column(db.Text())
    exit_name = db.Column(db.Text())


class OrganizationNatClass(AbstractClass):
    chain_name = db.Column(db.Text())
    nat_class = db.Column(db.Text())


def get_have_logos():
    have_logos = glob.glob("../static/map_icons/*")
    dic = {}
    for have_logo in have_logos:
        im = Image.open(have_logo)
        width, height = im.size
        square = width * height

        have_logo = have_logo.split("/")[-1]
        have_logo = ".".join(have_logo.split(".")[:-1])
        dic[have_logo] = width
    return dic


