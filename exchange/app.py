from threading import Thread

from exchange.data_base import Base, engine
from exchange.price_changer.price_changer import start_after_sleep
from flask import Flask

from .api import api


def create_app(test_call: bool = False) -> Flask:
    if not test_call:
        Thread(target=start_after_sleep).start()
    Base.metadata.create_all(engine)
    app: Flask = Flask(__name__)
    api.init_app(app)
    return app
