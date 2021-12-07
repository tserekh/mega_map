import pandas as pd
from sqlalchemy import create_engine

SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost:5433/postgres"
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
