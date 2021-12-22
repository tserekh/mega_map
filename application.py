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

from app import application

con = create_engine(application.config["SQLALCHEMY_DATABASE_URI"])
logging.info("Start initializing graph")
df_stops_for_routing = get_stops_for_routing(con)
df = get_graph_data(con)
G = build_graph(df)

logging.info("All ok with global variables")

@application.route("/", methods=["POST", "GET"])
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


@application.route("/get_metros", methods=["GET"])
def get_metros():
    coord_filter = create_coord_filter(request)
    df = pd.read_sql(f"select count(*) from  public.metros where {coord_filter}", con)
    count = df.iloc[0, 0]
    if count < 30:
        df = pd.read_sql(f"select * from public.metros where {coord_filter}", con)
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


@application.route("/get_ground_stops", methods=["GET"])
def get_ground_stops():
    n_clusters = 200
    agg = {"source_name": "size"}
    coord_filter = create_coord_filter(request)
    df = pd.read_sql(f"select * from public.bus_stops where {coord_filter}", con)
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


@application.route("/get_orgs", methods=["GET"])
def get_orgs():
    return {"orgs": []}


@application.route("/get_homes", methods=["GET"])
def get_homes():
    coord_filter = create_coord_filter(request)
    df_houses = pd.read_sql(f"select * from houses where {coord_filter}", con)
    n_clusters = 100
    agg = {"flat_num": "sum"}
    df_clusters = get_clusters(df_houses, n_clusters, agg, "stupid")
    context = {"homes": list(df_clusters.T.to_dict().values())}
    return context


@application.route("/get_route", methods=["GET"])
def get_route():
    if request.args.get("lat_start") is None:
        address_from = request.args.get("address_from")
        print(address_from)
        address_to = request.args.get("address_to")
        print(address_to)
        lat_start, lon_start = geocode(address_from)
        lat_end, lon_end = geocode(address_to)
    else:
        lat_start = float(request.args.get("lat_start"))
        lon_start = float(request.args.get("lon_start"))
        lat_end = float(request.args.get("lat_end"))
        lon_end = float(request.args.get("lon_end"))
    shortest_path_coords, shortest_path_nodes, total_weight = get_pretty_route(
        G, df, df_stops_for_routing, lat_start, lon_start, lat_end, lon_end
    )
    G.remove_node("start_point")
    G.remove_node("end_point")
    transformer = Transformer.from_crs("epsg:4326", "epsg:3857")

    start_coords_xy = transformer.transform(lat_start, lon_start)
    end_coords_xy = transformer.transform(lat_end, lon_end)
    short_route_names = list(
        map(lambda x: x.split("__")[-1], shortest_path_nodes[1:-1])
    )
    shortest_path_coords = (
        [start_coords_xy]
        + list(map(list, shortest_path_coords[["x", "y"]].values))
        + [end_coords_xy]
    )
    short_route_names = ["start_point"] + short_route_names + ["end_point"]
    return {
        "route": {
            "shortest_path_coords": shortest_path_coords,
            "short_route_names": short_route_names,
            "total_weight": total_weight,
            "start_coords_xy": start_coords_xy,
            "end_coords_xy": end_coords_xy,
        }
    }


if __name__ == "__main__":
    application.run(host="0.0.0.0", port=5000, debug=(not config.prod))