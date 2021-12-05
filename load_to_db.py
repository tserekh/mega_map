import pandas as pd
from sqlalchemy import create_engine

con = create_engine("postgresql://postgres:postgres@localhost/postgres")
data_path = "/home/tserekh"

df_homes = pd.read_csv(f"{data_path}/homes.csv", sep="\t").drop("Unnamed: 0", axis=1)
df_groud_stops = pd.read_csv(f"{data_path}/groud_stops.csv", sep="\t")
df_metros = pd.read_csv(f"{data_path}/metro.csv", sep="\t")

df_groud_stops.to_sql("groud_stops", con, "postgres", if_exists="replace")
df_metros.to_sql("metros", con, "postgres", if_exists="replace")
df_homes.to_sql("homes", con, "postgres", if_exists="replace")
