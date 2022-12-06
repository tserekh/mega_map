import pandas as pd
from sqlalchemy import create_engine

from config import SQLALCHEMY_DATABASE_URI

con = create_engine(SQLALCHEMY_DATABASE_URI)

df = pd.read_csv("external_data/houses.csv", sep=";")
con.execute("delete from public.houses")
df.to_sql("houses", con, "public", if_exists="append", index=False)


df = pd.read_csv("external_data/metros.csv", sep=";")
con.execute("delete from public.metros")
df.to_sql("metros", con, "public", if_exists="append", index=False)

df = pd.read_csv("external_data/bus_stops.csv", sep="\t")
con.execute("delete from public.bus_stops")
df.to_sql("bus_stops", con, "public", if_exists="append", index=False)

df = pd.read_csv("external_data/graph.csv", sep=";")
con.execute("delete from public.graph")
df.to_sql("graph", con, "public", if_exists="append", index=False)


df = pd.read_csv("external_data/trip_short.csv", sep=";")
# df = df[~df["short_name"].apply(lambda x: x.startswith("Н"))]
con.execute("delete from public.trip_short")
df.to_sql("trip_short", con, "public", if_exists="append", index=False)

