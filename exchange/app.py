from exchange.data_base import Database
from exchange.m import s
from flask import Flask


def create_app() -> Flask:
    Database.create()
    app: Flask = Flask(__name__)
    app.register_blueprint(s)
    return app
