from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

import config
from model import db

app = Flask(__name__)
app.debug = config.DEBUG
app.config["SQLALCHEMY_DATABASE_URI"] = config.DB_URI
db.init_app(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command("db", MigrateCommand)

if __name__ == "__main__":
    manager.run()