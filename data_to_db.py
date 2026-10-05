import os

import pandas as pd
from sqlalchemy import create_engine, text

from app import application, db

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "external_data")

# (таблица, csv-файл, разделитель)
TABLES = [
    ("houses", "houses.csv", ";"),
    ("metros", "metros.csv", ";"),
    ("bus_stops", "bus_stops.csv", "\t"),
    ("graph", "graph.csv", ";"),
    ("trip_short", "trip_short.csv", ";"),
]

con = create_engine(application.config["SQLALCHEMY_DATABASE_URI"])
# Создаём таблицы, если их ещё нет
db.metadata.create_all(con)

for table, filename, sep in TABLES:
    path = os.path.join(DATA_DIR, filename)
    print(f"Загрузка {path} -> {table}")
    df = pd.read_csv(path, sep=sep)
    # df = df[~df["short_name"].apply(lambda x: x.startswith("Н"))]  # для trip_short
    # Очистка и загрузка в одной транзакции: при ошибке старые данные останутся
    with con.begin() as conn:
        conn.execute(text(f"delete from {table}"))
        df.to_sql(table, conn, if_exists="append", index=False, chunksize=10000)
    print(f"Готово: {len(df)} строк")

con.dispose()
