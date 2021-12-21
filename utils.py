import pandas as pd


def get_clusters(df, n_clusters, agg, mode):
    if len(df) == 0:
        return pd.DataFrame()
    # if "x" not in df.columns:
    #     df["xy"] = df.apply(add3857, axis=1)
    #     df["x"] = df["xy"].apply(lambda xy: xy[0])
    #     df["y"] = df["xy"].apply(lambda xy: xy[1])
    #     df = df.drop(["xy", "lat", "lon"], axis=1)

    xy = ["x", "y"]

    if n_clusters < len(df):
        if mode == "clever":
            raise NotImplementedError
            # agg["x"] = "size"
            # kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(df[xy])
            # df["cluster_label"] = kmeans.labels_
            #
            # df_clusters = df.groupby("cluster_label").agg(agg).reset_index()
            # df_clusters = df_clusters.reset_index()
            # df_clusters = df_clusters.rename(columns={"x": "count"})
            # df_clusters["is_one"] = df_clusters["count"] != 1
            # df_cluster_centers = pd.DataFrame(kmeans.cluster_centers_, columns=xy)
            # df_cluster_centers["cluster_label"] = df_cluster_centers.index
            # df_clusters = pd.merge(df_clusters, df_cluster_centers, on="cluster_label")
            # df_clusters.drop("cluster_label", axis=1, inplace=True)
        elif mode == "stupid":

            delta_x = df["x"].max() - df["x"].min()
            delta_y = df["y"].max() - df["y"].min()
            square_side = (delta_x * delta_y / n_clusters) ** 0.5
            df["x_round"] = df["x"].apply(
                lambda x: square_side * round(x / square_side)
            )
            df["y_round"] = df["y"].apply(
                lambda x: square_side * round(x / square_side)
            )

            agg["source_name"] = "size"
            agg["x"] = "mean"
            agg["y"] = "mean"
            df_clusters = (
                df.groupby(["x_round", "y_round"])
                .agg(agg)
                .rename(columns={"source_name": "count"})
                .reset_index()
            )
            df_clusters["is_one"] = df_clusters["count"] == 1
            df_clusters = df_clusters.reindex()
        else:
            assert False, "Incorrect cluster mode"

    else:
        df_clusters = df[xy + list(agg.keys())]
        df_clusters["count"] = 1
        df_clusters["is_one"] = True
        for key in agg.keys():
            if agg[key] == "size":
                df_clusters[key] = 1
                break
    return df_clusters
