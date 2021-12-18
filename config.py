import os

prod = True
if prod:
    # SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL'].replace("postgres://", "postgresql://")
    SQLALCHEMY_DATABASE_URI = os.environ["HEROKU_POSTGRESQL_CYAN_URL"].replace(
        "postgres://", "postgresql://"
    )

    # SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@postgres:5432/postgres"

else:
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost:5433/postgres"

### routing area
lat_max, lon_max = 55.901923, 37.607278
lat_min, lon_min = 55.848597, 37.524299
