from functools import reduce
from itertools import product
from typing import Iterable, List, Tuple

import networkx as nx
import pandas as pd
from networkx.classes.function import path_weight
from pyproj import Transformer
from sklearn.neighbors import KDTree

import config


def get_pairs(arr):
    return list(filter(lambda x: x[0] != x[1], product(arr, arr)))


def get_graph_data(con):
    return pd.read_sql("select * from public.graph", con)


def build_graph(df: pd.DataFrame, df_stop: pd.DataFrame) -> nx.classes.digraph.DiGraph:
    df_route_graph = df[df["using_trip_id__next"] == df["using_trip_id"]]

    df_transfers_to_stop = df.groupby("stop_id").agg({"stop_id__using_trip_id": list})

    only_one_trip_stops = df_transfers_to_stop[
        df_transfers_to_stop["stop_id__using_trip_id"].apply(len) == 1
    ]["stop_id__using_trip_id"].index

    transfer_nodes = df[df["stop_id"].isin(only_one_trip_stops)][
        ["stop_id__using_trip_id", "stop_id"]
    ]
    transfer_nodes["time"] = 1.5

    G = nx.DiGraph()
    G.add_weighted_edges_from(
        df_route_graph[
            ["stop_id__using_trip_id", "stop_id__using_trip_id__next", "time"]
        ].values
    )
    G.add_weighted_edges_from(
        transfer_nodes[["stop_id__using_trip_id", "stop_id", "time"]].values
    )
    G.add_weighted_edges_from(
        transfer_nodes[["stop_id", "stop_id__using_trip_id", "time"]].values
    )

    stop_stop_nodes = pd.DataFrame()
    k = 20
    for j in range(1, k):
        tree = KDTree(df_stop[["x", "y"]], leaf_size=40)
        dists, inds = tree.query(df_stop[["x", "y"]], k=k)

        df_stop["stop_id_2"] = df_stop.iloc[inds[:, j]]["stop_id"].values
        df_stop["dist"] = dists[:, j]

        stop_stop_nodes = stop_stop_nodes.append(
            df_stop[["stop_id", "stop_id_2", "dist"]]
        )
        stop_stop_nodes["time"] = stop_stop_nodes["dist"] / 118.0

    G.add_weighted_edges_from(stop_stop_nodes[["stop_id", "stop_id_2", "time"]].values)
    G.add_weighted_edges_from(stop_stop_nodes[["stop_id_2", "stop_id", "time"]].values)

    return G


def get_potential_start_and_end(
    df: pd.DataFrame,
    df_stop: pd.DataFrame,
    start_coords_xy: (float, float),
    end_coords_xy: (float, float),
) -> (pd.DataFrame, pd.DataFrame):
    speed_met_in_min = 118
    tree = KDTree(df_stop[["x", "y"]], leaf_size=40)
    dists, inds = tree.query([start_coords_xy, end_coords_xy], k=50)
    df_start_stop = df_stop.iloc[inds[0]].copy()
    df_end_stop = df_stop.iloc[inds[1]].copy()

    df_start_stop["dist"] = dists[0]
    df_end_stop["dist"] = dists[1]
    df_start_stop["time"] = df_start_stop["dist"] / speed_met_in_min
    df_end_stop["time"] = df_end_stop["dist"] / speed_met_in_min

    df_potential_start = pd.merge(
        df[["stop_id", "using_trip_id", "stop_id__using_trip_id"]],
        df_start_stop[["stop_id", "time"]],
        on="stop_id",
    )
    df_potential_end = pd.merge(
        df[["stop_id", "using_trip_id", "stop_id__using_trip_id"]],
        df_end_stop[["stop_id", "time"]],
        on="stop_id",
    )

    df_potential_start["start_point"] = "start_point"
    df_potential_end["end_point"] = "end_point"

    df_potential_start = df_potential_start[
        ["start_point", "stop_id__using_trip_id", "time"]
    ]
    df_potential_end = df_potential_end[["stop_id__using_trip_id", "end_point", "time"]]
    return df_potential_start, df_potential_end


def get_stops_for_routing(con):

    return pd.read_sql(
        f"""select * from public.bus_stops where
    lat>={config.lat_min} and lat<={config.lat_max} and lon>={config.lon_min} and lon<={config.lon_max}
                       """,
        con,
    )


def get_route(
    G: nx.classes.digraph.DiGraph,
    df_stop: pd.DataFrame,
    df_trip_id__short_name: pd.DataFrame,
):
    shortest_path_nodes = nx.shortest_path(
        G, "start_point", "end_point", weight="weight"
    )
    weight = path_weight(G, shortest_path_nodes, weight="weight")

    pretty_nodes = []
    xy_list = []
    for node in shortest_path_nodes[1:-1]:
        if "__" in str(node):
            trip_id = node.split("__")[-1]
            stop_id = node.split("__")[0]
            trip_df = df_trip_id__short_name[
                df_trip_id__short_name["trip_id"] == trip_id
            ]
            if len(trip_df) > 0:
                short_name = trip_df["short_name"].iloc[0]
            else:
                short_name = trip_id
            pretty_nodes.append(short_name)
        else:
            stop_id = str(node)
            pretty_nodes.append(stop_id)

        stop_xy = list(
            df_stop[df_stop["stop_id"] == int(float(stop_id))][["x", "y"]].iloc[0]
        )
        xy_list.append(stop_xy)
    print(pretty_nodes)
    return xy_list, pretty_nodes, weight


def get_trip_short(con) -> pd.DataFrame:
    return pd.read_sql(
        "select * from public.trip_short",
        con,
    )


def get_pretty_route(
    G: nx.classes.digraph.DiGraph,
    df: pd.DataFrame,
    df_stop: pd.DataFrame,
    df_trip_id__short_name: pd.DataFrame,
    lat_start: float,
    lon_start: float,
    lat_end: float,
    lon_end: float,
) -> Tuple[List, List, float]:
    transformer = Transformer.from_crs("epsg:4326", "epsg:3857")
    start_coords_xy = transformer.transform(lat_start, lon_start)
    end_coords_xy = transformer.transform(lat_end, lon_end)

    df_potential_start, df_potential_end = get_potential_start_and_end(
        df, df_stop, start_coords_xy, end_coords_xy
    )
    G.add_weighted_edges_from(df_potential_start.values)
    G.add_weighted_edges_from(df_potential_end.values)
    xy_list, pretty_nodes, weight = get_route(G, df_stop, df_trip_id__short_name)
    return xy_list, pretty_nodes, weight
