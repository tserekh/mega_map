import os

# SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL'].replace("postgres://", "postgresql://")
os.environ["DATABASE_URL"] = "postgres://postgres:postgres@db:5432/postgres"
SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"].replace(
    "postgres://", "postgresql://"
)
### routing area
lat_max, lon_max = 56.0, 38.0
lat_min, lon_min = 55.0, 37.0
