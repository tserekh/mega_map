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
lat_max, lon_max = 56.0, 38.0
lat_min, lon_min = 55.0, 37.0
