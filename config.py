import os
prod = True
if prod:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL'].replace("postgres://", "postgresql://")
    # SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@postgres:5432/postgres"

else:
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost:5433/postgres"
