from functools import reduce
from itertools import product

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


def build_graph(df):

    df_route_graph = df[df["route_short_name__next"] == df["route_short_name"]]
    df_transfer = (
        df.groupby("stop_id").agg({"stop_id__route_short_name": list}).reset_index()
    )
    df_transfer = df_transfer[df_transfer["stop_id__route_short_name"].apply(len) > 1]
    transfer_list = list(
        map(lambda x: tuple(x), df_transfer["stop_id__route_short_name"].values)
    )

    transfer_nodes = reduce(lambda x, y: x + y, (map(get_pairs, transfer_list)))
    transfer_nodes = list(map(lambda x: (x[0], x[1], 5), transfer_nodes)) + list(
        map(lambda x: (x[1], x[0], 5), transfer_nodes)
    )

    G = nx.DiGraph()
    G.add_weighted_edges_from(
        df_route_graph[
            ["stop_id__route_short_name", "stop_id__route_short_name__next", "time"]
        ].values
    )
    G.add_weighted_edges_from(transfer_nodes)
    return G


def get_potentilal_start_and_end(df, df_stop, start_coords_xy, end_coords_xy):
    speed_met_in_min = 66
    tree = KDTree(df_stop[["x", "y"]], leaf_size=40)
    dists, inds = tree.query([start_coords_xy, end_coords_xy], k=10)
    df_start_stop = df_stop.iloc[inds[0]].copy()
    df_end_stop = df_stop.iloc[inds[1]].copy()

    df_start_stop["dist"] = dists[0]
    df_end_stop["dist"] = dists[1]
    df_start_stop["time"] = df_start_stop["dist"] / speed_met_in_min
    df_end_stop["time"] = df_end_stop["dist"] / speed_met_in_min

    df_potential_start = pd.merge(
        df[["stop_id", "route_short_name", "stop_id__route_short_name"]],
        df_start_stop[["stop_id", "time"]],
        on="stop_id",
    )
    df_potential_end = pd.merge(
        df[["stop_id", "route_short_name", "stop_id__route_short_name"]],
        df_end_stop[["stop_id", "time"]],
        on="stop_id",
    )

    df_potential_start["start_point"] = "start_point"
    df_potential_end["end_point"] = "end_point"

    df_potential_start = df_potential_start[
        ["start_point", "stop_id__route_short_name", "time"]
    ]
    df_potential_end = df_potential_end[
        ["stop_id__route_short_name", "end_point", "time"]
    ]
    return df_potential_start, df_potential_end


def get_stops_for_routing(con):

    return pd.read_sql(
        f"""select * from public.bus_stops where
    lat>={config.lat_min} and lat<={config.lat_max} and lon>={config.lon_min} and lon<={config.lon_max}
                       """,
        con,
    )


def get_route(G, df_stop):
    shortest_path_nodes = nx.shortest_path(
        G, "start_point", "end_point", weight="weight"
    )
    weight = path_weight(G, shortest_path_nodes, weight="weight")
    route_stop_ids = list(
        map(lambda x: int(x.split("__")[0]), shortest_path_nodes[1:-1])
    )
    df_route_stop_ids = pd.DataFrame(route_stop_ids, columns=["stop_id"])
    df_route_stop_ids = df_route_stop_ids.reset_index().rename(
        columns={"index": "stop_num"}
    )
    shortest_path_coords = pd.merge(
        df_stop, df_route_stop_ids, on="stop_id"
    ).sort_values("stop_num")
    return shortest_path_coords, shortest_path_nodes, weight


def get_pretty_route(G, df, df_stop, lat_start, lon_start, lat_end, lon_end):
    transformer = Transformer.from_crs("epsg:4326", "epsg:3857")
    start_coords_xy = transformer.transform(lat_start, lon_start)
    end_coords_xy = transformer.transform(lat_end, lon_end)

    df_potential_start, df_potential_end = get_potentilal_start_and_end(
        df, df_stop, start_coords_xy, end_coords_xy
    )
    G.add_weighted_edges_from(df_potential_start.values)
    G.add_weighted_edges_from(df_potential_end.values)
    shortest_path_coords, shortest_path_nodes, weight = get_route(G, df_stop)
    return shortest_path_coords, shortest_path_nodes, weight
