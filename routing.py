from itertools import product
from typing import List, Tuple

import networkx as nx
import pandas as pd
from networkx.classes.function import path_weight
from pyproj import Transformer
from sklearn.neighbors import KDTree


def get_pairs(arr):
    return list(filter(lambda x: x[0] != x[1], product(arr, arr)))


def get_graph_data(con):

    return pd.read_sql(
        """select     stop_id,
    using_trip_id,
    using_trip_id__next,
    stop_id__using_trip_id,
    stop_id__using_trip_id__next,
    time from public.graph""",
        con,
    )


def build_graph(df: pd.DataFrame, df_stop: pd.DataFrame) -> nx.classes.digraph.DiGraph:
    speed_met_in_min = 118.0 / 3
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
    k = 40
    for j in range(1, k):
        tree = KDTree(df_stop[["x", "y"]], leaf_size=40)
        dists, inds = tree.query(df_stop[["x", "y"]], k=k)

        df_stop["stop_id_2"] = df_stop.iloc[inds[:, j]]["stop_id"].values
        df_stop["dist"] = dists[:, j]

        stop_stop_nodes = stop_stop_nodes.append(
            df_stop[["stop_id", "stop_id_2", "dist"]]
        )
        stop_stop_nodes["time"] = stop_stop_nodes["dist"] / speed_met_in_min
    G.add_weighted_edges_from(stop_stop_nodes[["stop_id", "stop_id_2", "time"]].values)
    G.add_weighted_edges_from(stop_stop_nodes[["stop_id_2", "stop_id", "time"]].values)
    return G


def get_potential_start_and_end(
    df_stop: pd.DataFrame,
    start_coords_xy: (float, float),
    end_coords_xy: (float, float),
) -> (pd.DataFrame, pd.DataFrame):
    speed_met_in_min = 118 / 3
    tree = KDTree(df_stop[["x", "y"]], leaf_size=50)
    dists, inds = tree.query([start_coords_xy, end_coords_xy], k=50)
    df_start_stop = df_stop.iloc[inds[0]].copy()
    df_end_stop = df_stop.iloc[inds[1]].copy()
    df_start_stop["dist"] = dists[0]
    df_end_stop["dist"] = dists[1]
    df_start_stop["time"] = df_start_stop["dist"] / speed_met_in_min
    df_end_stop["time"] = df_end_stop["dist"] / speed_met_in_min
    df_start_stop["start_point"] = "start_point"
    df_end_stop["end_point"] = "end_point"

    return (
        df_start_stop[["start_point", "stop_id", "time"]],
        df_end_stop[["stop_id", "end_point", "time"]],
    )


def get_stops_for_routing(con):

    return pd.read_sql(
        "select * from public.bus_stops",
        con,
    )


def stop_by_id(df_stop: pd.DataFrame, stop_id: str) -> pd.Series:
    if (stop_id == "start_point") or (stop_id == "end_point"):
        return pd.Series({"x": None, "y": None, "stop_name": stop_id})
    stop_id = int(float(stop_id))
    return (
        df_stop[df_stop["stop_id"].astype(int) == stop_id].iloc[0]
    )


def trip_id_to_short_name(trip_id: str, df_trip_id__short_name: pd.DataFrame):
    return df_trip_id__short_name[df_trip_id__short_name["trip_id"] == trip_id].iloc[0]["short_name"]


def format_sub_paths(nodes_list: List[List[str]], df_stop: pd.DataFrame) -> List[str]:
    """
    Получаем маршрут в человекочитаемом виде
    """
    formatted = []
    for sub_path in nodes_list:
        if '__' in str(sub_path[-1]):
            route_name = str(sub_path[-1]).split("_")[-1]
            formatted.append(f"Проехать {len(sub_path)-1} остановок на маршруте {route_name}")
        elif str(sub_path[-1]) == 'end_point':
            formatted.append(f"Дойти до конечной точки")
        else:
            stop_id = sub_path[-1]
            stop_name = stop_by_id(df_stop, stop_id)["stop_name"]
            formatted.append(f"Дойти до остановки {stop_name}")
    return formatted


def get_name_from_node(node: str, df_trip_id__short_name: pd.DataFrame, df_stop: pd.DataFrame):
    if "__" in node:
        # маршрут-остановка
        stop_id, trip_id = node.split("__")
        return trip_id_to_short_name(trip_id, df_trip_id__short_name)
    elif node == "end_point":
        return "end_point"
    else:
        # остановка
        stop_id = node
        return stop_by_id(df_stop, stop_id)["stop_name"]


def get_xy_coord_from_node(node: str, df_stop: pd.DataFrame):
    if "__" in node:
        # маршрут-остановка
        stop_id, trip_id = node.split("__")
    elif (node == "start_point") or (node == "end_point"):
        return [None, None]
    else:
        # остановка
        stop_id = node
    return list(stop_by_id(df_stop, stop_id)[["x", "y"]])


def get_route(
    G: nx.classes.digraph.DiGraph,
    df_stop: pd.DataFrame,
    df_trip_id__short_name: pd.DataFrame,
):
    shortest_path_nodes = nx.shortest_path(
        G, "start_point", "end_point", weight="weight"
    )
    print(shortest_path_nodes)
    weight = path_weight(G, shortest_path_nodes, weight="time")
    names_list = []
    names = [shortest_path_nodes[0]]
    xy_coords_list = []
    xy_coords = [shortest_path_nodes[0]]
    nodes_list = []
    nodes = [shortest_path_nodes[0]]
    in_bus = False
    for node in shortest_path_nodes[1:]:
        name = get_name_from_node(str(node), df_trip_id__short_name, df_stop)
        xy_coord = get_xy_coord_from_node(str(node), df_stop)
        if in_bus ^ ("__" in str(node)):
            names_list.append(names)
            xy_coords_list.append(xy_coords)
            nodes_list.append(nodes)
            names = [name]
            xy_coords = [xy_coord]
            nodes = [node]
            in_bus = not in_bus
        else:
            names.append(name)
            xy_coords.append(xy_coord)
            nodes.append(node)
    return xy_coords_list, format_sub_paths(nodes_list, df_stop), weight


def get_trip_short(con) -> pd.DataFrame:
    return pd.read_sql(
        "select * from public.trip_short",
        con,
    )


def get_pretty_route(
    G: nx.classes.digraph.DiGraph,
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
        df_stop, start_coords_xy, end_coords_xy
    )
    G.add_weighted_edges_from(df_potential_start.values)
    G.add_weighted_edges_from(df_potential_end.values)
    xy_list, pretty_nodes, weight = get_route(G, df_stop, df_trip_id__short_name)
    return xy_list, pretty_nodes, weight
