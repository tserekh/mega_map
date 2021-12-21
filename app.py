import glob
import logging

import pandas as pd
from flask import Flask, g, render_template, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from PIL import Image
from pyproj import Transformer
from sqlalchemy import create_engine

import config
from config import SQLALCHEMY_DATABASE_URI
from geocode import geocode
from routing import (build_graph, get_graph_data, get_pretty_route,
                     get_stops_for_routing)
from utils import get_clusters

application = Flask(__name__)
application.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
con = create_engine(application.config["SQLALCHEMY_DATABASE_URI"])

db = SQLAlchemy(application)
migrate = Migrate(application, db)

class AbstractClass:
    id = db.Column(db.Integer, primary_key=True)
    stop_id = db.Column(db.Integer())
    lat = db.Column(db.Float())
    lon = db.Column(db.Float())

    x = db.Column(db.Float())
    y = db.Column(db.Float())

    source_name = db.Column(db.Text())
    info = db.Column(db.Text())


class Houses(db.Model, AbstractClass):
    flat_num = db.Column(db.Float())
    address = db.Column(db.Text())


class Metros(db.Model, AbstractClass):
    station_name = db.Column(db.Text())
    exit_name = db.Column(db.Text())


class BusStops(db.Model, AbstractClass):
    stop_name = db.Column(db.Text())


class Graph(db.Model, AbstractClass):
    trip_id = db.Column(db.Text())
    stop_id = db.Column(db.Integer())
    stop_sequence = db.Column(db.Integer())
    route_id = db.Column(db.Integer())
    service_id = db.Column(db.Integer())
    route_short_name = db.Column(db.Text())
    route_short_name__next = db.Column(db.Text())
    stop_id__route_short_name = db.Column(db.Text())
    stop_id__route_short_name__next = db.Column(db.Text())
    time = db.Column(db.Float())