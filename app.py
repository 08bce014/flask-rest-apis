from flask import Flask
import config
from model import db
from resource import products_api


"""Creating flask app"""
app = Flask(__name__)

app.config['DEBUG'] = True

app.config["SQLALCHEMY_DATABASE_URI"] = config.DB_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config.SQLALCHEMY_TRACK_MODIFICATIONS
db.init_app(app)
db.app = app

app.register_blueprint(products_api, url_prefix='/products/')

if __name__ == '__main__':
    app.run(host=config.HOST, port=config.PORT, debug=True)
