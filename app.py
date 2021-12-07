import glob

import pandas as pd
from flask import Flask, render_template, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from PIL import Image
from sqlalchemy import create_engine
from config import SQLALCHEMY_DATABASE_URI
from utils import get_clusters

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.secret_key = 'secret string'
con = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])


db = SQLAlchemy(app)
migrate = Migrate(app, db)


class AbstractClass:
    id = db.Column(db.Integer, primary_key=True)
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
    station_name = db.Column(db.Text())


# class OrganizationNatClass(db.Model, AbstractClass):
#     chain_name = db.Column(db.Text())
#     nat_class = db.Column(db.Text())


@app.route("/", methods=["POST", "GET"])
def show_map():
    return render_template("points.html", have_logos=get_have_logos())


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


def create_coord_filter(request):
    lat_min = float(request.args.get("lat_min"))
    lon_min = float(request.args.get("lon_min"))
    lat_max = float(request.args.get("lat_max"))
    lon_max = float(request.args.get("lon_max"))
    coord_filter = (
        f"lat>={lat_min} and lat<={lat_max} and lon>={lon_min} and lon<={lon_max}"
    )
    return coord_filter


@app.route("/get_metros", methods=["GET"])
def get_metros():
    coord_filter = create_coord_filter(request)
    df = pd.read_sql(
        f"select count(*) from public.metros {coord_filter}", con
    )
    count = df.iloc[0, 0]
    if count < 30:
        df = pd.read_sql(
            f"select * from public.metros where {coord_filter}", con
        )
    else:
        df = pd.read_sql(
            f"""
            select avg(x) as x, avg(y) as y, avg(lat) as lat, avg(lon) as lon, station_name, 'Нет информации' as info
            from public.metros
            where {coord_filter}
            group by station_name
            """,
            con,
        )
    result = list(df.T.to_dict().values())
    return {"metros": result}


@app.route("/get_ground_stops", methods=["GET"])
def get_ground_stops():
    n_clusters = 200
    agg = {"source_name": "size"}
    coord_filter = create_coord_filter(request)
    df = pd.read_sql(
        f"select * from public.bus_stops where {coord_filter}", con
    )
    if len(df):
        df_clusters = get_clusters(df, n_clusters, agg, "stupid")
        df_clusters.rename(columns={"source_name": "n_ground_stops"}, inplace=True)
        context = {
            "ground_stops": list(df_clusters.T.to_dict().values()),
        }
    else:
        context = {
            "ground_stops": [],
        }
    return context


@app.route("/get_orgs", methods=["GET"])
def get_orgs():
    return {"orgs": []}


@app.route("/get_homes", methods=["GET"])
def get_homes():
    coord_filter = create_coord_filter(request)
    df = pd.read_sql(f"select * from houses where {coord_filter}", con)
    n_clusters = 100
    agg = {"flat_num": "sum"}
    df_clusters = get_clusters(df, n_clusters, agg, "stupid")
    context = {"homes": list(df_clusters.T.to_dict().values())}
    return context


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
