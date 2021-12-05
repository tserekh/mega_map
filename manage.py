from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command("db", MigrateCommand)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))


if __name__ == "__main__":
    manager.run()


class AbstractObject(db.Model):
    class Meta:
        abstract = True

    lat = db.Column(db.Float())
    lon = db.Column(db.Float())

    x = db.Column(db.Float())
    y = db.Column(db.Float())

    address = db.Column(db.Text())
    source_id = db.Column(db.Text())
    source_name = db.Column(db.Text())


class MetroStation(AbstractObject):
    station_name = db.Column(db.Text())
    info = db.Column(db.Text())


class Metro(AbstractObject):
    station_name = db.Column(db.Text())
    exit_name = db.Column(db.Text())
    info = db.Column(db.Text())


class OrganizationNatClass(AbstractObject):
    chain_name = db.Column(db.Text())
    nat_class = db.Column(db.Text())


if __name__ == "__main__":
    manager.run()
