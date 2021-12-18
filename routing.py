import datetime
import glob
import json
from functools import reduce
from itertools import product

import networkx as nx
import pandas as pd
from pyproj import Transformer
from sklearn.neighbors import KDTree


def get_pairs(arr):
    return list(filter(lambda x: x[0] != x[1], product(arr, arr)))


def to_datetime(x):
    extra_delta = datetime.timedelta(days=0)
    hour = x.split(":")[0]
    if hour in map(str, range(24, 48)):
        hour = int(hour) - 24
        x = str(hour) + ":" + ":".join(x.split(":")[1:])
        extra_delta = datetime.timedelta(days=1)
    x = datetime.datetime.strptime(x, "%H:%M:%S")
    return x + extra_delta


def get_stops(lat_max, lon_max, lat_min, lon_min):
    transformer = Transformer.from_crs("epsg:4326", "epsg:3857")
    df_stop = pd.read_csv(
        "D:/data/data_mos/tables/data-101781-2021-11-25.csv", sep=";", encoding="cp1251"
    )
    df_stop["coords"] = df_stop["geodata_center"].apply(
        lambda x: json.loads(x)["coordinates"]
    )
    df_stop["lon"] = df_stop["coords"].apply(lambda x: x[0])
    df_stop["lat"] = df_stop["coords"].apply(lambda x: x[1])
    df_stop["xy"] = df_stop[["lon", "lat"]].apply(
        lambda row: transformer.transform(row["lon"], row["lat"]), axis=1
    )
    df_stop["x"] = df_stop["xy"].apply(lambda x: x[0])
    df_stop["y"] = df_stop["xy"].apply(lambda x: x[1])
    df_stop = df_stop[
        (df_stop["lat"] > lat_min)
        & (df_stop["lon"] > lon_min)
        & (df_stop["lat"] < lat_max)
        & (df_stop["lon"] < lon_max)
    ]
    return df_stop


def get_data_list():
    json_paths = glob.glob("D:/data/data_mos/json/*")
    data_list_app = []
    for i, json_path in enumerate(json_paths):
        if (i % 500) == 0:
            print(i, end=" ")
        with open(json_path) as f:
            data_list = json.loads(f.read())
        if len(data_list) < 5:
            continue
        data_list = list(map(lambda x: x["Cells"], data_list))

        data_list_app += data_list
    return data_list_app


def prepare_data(data_list_app, lat_max, lon_max, lat_min, lon_min):
    df = pd.DataFrame(data_list_app)
    df = df.drop_duplicates()
    df = df[
        [
            "global_id",
            "trip_id",
            "arrival_time",
            "departure_time",
            "stop_id",
            "stop_sequence",
        ]
    ]

    df_stop = get_stops(lat_max, lon_max, lat_min, lon_min)
    df_weekdays = pd.read_csv(
        "D:/data/data_mos/tables/data-101785-2021-11-23.csv", sep=";", encoding="cp1251"
    )[
        [
            "service_id",
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday",
            "start_date",
            "end_date",
        ]
    ]
    df_route_names = pd.read_csv(
        "D:/data/data_mos/tables/data-101782-2021-11-23.csv", sep=";", encoding="cp1251"
    )
    df_service = pd.read_csv(
        "D:/data/data_mos/tables/data-101783-2021-11-23.csv", sep=";", encoding="cp1251"
    )

    df_service_w_route_names = pd.merge(
        df_service[["route_id", "trip_id", "service_id"]],
        df_route_names[["route_id", "route_short_name", "route_long_name"]],
        on="route_id",
    )
    df = pd.merge(df, df_service_w_route_names, on="trip_id")
    df = pd.merge(df, df_stop, on="stop_id")
    df = pd.merge(df, df_weekdays, on="service_id")

    df["start_date"] = df["start_date"].astype(str)
    df["end_date"] = df["end_date"].astype(str)
    weekday = "monday"
    week_cols = [
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
    ]
    df = df[df[weekday] == 1].drop(week_cols, axis=1).copy()

    df_gb = pd.DataFrame(
        df.groupby(["trip_id", "route_short_name"]).size()
    ).reset_index()
    df_gb_max = df_gb.groupby("route_short_name", as_index=False).agg({0: "max"})
    df_merge = pd.merge(df_gb, df_gb_max, on="route_short_name")
    trip_ids = (
        df_merge[df_merge["0_x"] == df_merge["0_y"]]
        .drop_duplicates("route_short_name")["trip_id"]
        .values
    )
    df["stop_id-route_short_name"] = (
        df["stop_id"].astype(str) + "__" + df["route_short_name"]
    )
    df = df.sort_values(["trip_id", "stop_sequence"])

    df["stop_id-route_short_name__next"] = df["stop_id-route_short_name"].shift(-1)
    df["route_short_name__next"] = df["route_short_name"].shift(-1)
    df["departure_time__next"] = df["departure_time"].shift(-1)
    df = df.iloc[:-1]

    df["time"] = df["departure_time__next"].apply(to_datetime) - df[
        "departure_time"
    ].apply(to_datetime)
    df["time"] = df["time"].apply(lambda x: x.total_seconds() / 60)
    return df


def build_graph(df):
    df_route_graph = df[df["route_short_name__next"] == df["route_short_name"]]
    df_transfer = (
        df.groupby("stop_id").agg({"stop_id-route_short_name": list}).reset_index()
    )
    df_transfer = df_transfer[df_transfer["stop_id-route_short_name"].apply(len) > 1]
    transfer_list = list(
        map(lambda x: tuple(x), df_transfer["stop_id-route_short_name"].values)
    )

    transfer_nodes = reduce(lambda x, y: x + y, (map(get_pairs, transfer_list)))
    transfer_nodes = list(map(lambda x: (x[0], x[1], 5), transfer_nodes)) + list(
        map(lambda x: (x[1], x[0], 5), transfer_nodes)
    )

    G = nx.DiGraph()
    G.add_weighted_edges_from(
        df_route_graph[
            ["stop_id-route_short_name", "stop_id-route_short_name__next", "time"]
        ].values
    )
    G.add_weighted_edges_from(transfer_nodes)
    return G


def get_potenstilal_start_and_end(df_stop, start_coords_xy, end_coords_xy):

    tree = KDTree(df_stop[["x", "y"]], leaf_size=40)

    dists, inds = tree.query([start_coords_xy, end_coords_xy], k=10)

    df_start_stop = df_stop.iloc[inds[0]].copy()
    df_end_stop = df_stop.iloc[inds[1]].copy()

    df_start_stop["dist"] = dists[0]
    df_end_stop["dist"] = dists[1]
    #     print(inds[0])
    #     print(inds[1])
    speed_met_in_min = 66  # 4 km/h

    df_start_stop["time"] = df_start_stop["dist"] / 66
    df_end_stop["time"] = df_end_stop["dist"] / 66

    df_potential_start = pd.merge(
        df[["stop_id", "route_short_name", "stop_id-route_short_name"]],
        df_start_stop[["stop_id", "time"]],
        on="stop_id",
    )
    df_potential_end = pd.merge(
        df[["stop_id", "route_short_name", "stop_id-route_short_name"]],
        df_end_stop[["stop_id", "time"]],
        on="stop_id",
    )

    df_potential_start["start_point"] = "start_point"
    df_potential_end["end_point"] = "end_point"

    df_potential_start = df_potential_start[
        ["start_point", "stop_id-route_short_name", "time"]
    ]
    df_potential_end = df_potential_end[
        ["stop_id-route_short_name", "end_point", "time"]
    ]
    return df_potential_start, df_potential_end


def get_route(G, df_stop):
    shortest_path = nx.shortest_path(G, "start_point", "end_point")
    route_stop_ids = list(map(lambda x: int(x.split("__")[0]), shortest_path[1:-1]))
    df_route_stop_ids = pd.DataFrame(route_stop_ids, columns=["stop_id"])
    df_route_stop_ids = df_route_stop_ids.reset_index().rename(
        columns={"index": "stop_num"}
    )
    vc = pd.Series(route_stop_ids).value_counts()
    transfer_stop_ids = vc[vc > 1].index
    qqq = pd.merge(df_stop, df_route_stop_ids, on="stop_id").sort_values("stop_num")
    return qqq, shortest_path, transfer_stop_ids


def get_result(G, df_stop, start_coords, end_coords):
    transformer = Transformer.from_crs("epsg:4326", "epsg:3857")
    start_coords_xy = transformer.transform(*start_coords[::-1])
    end_coords_xy = transformer.transform(*end_coords[::-1])

    df_potential_start, df_potential_end = get_potenstilal_start_and_end(
        df_stop, start_coords_xy, end_coords_xy
    )
    G.add_weighted_edges_from(df_potential_start.values)
    G.add_weighted_edges_from(df_potential_end.values)
    qqq, shortest_path, transfer_stop_ids = get_route(G, df_stop)
    return qqq, shortest_path, transfer_stop_ids, start_coords_xy, end_coords_xy


df_stop = get_stops(lat_max, lon_max, lat_min, lon_min)
