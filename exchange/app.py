from exchange.data_base import Database
from flask import Flask

from .api import api


def create_app() -> Flask:
    Database.create()
    app: Flask = Flask(__name__)
    api.init_app(app)
    return app
