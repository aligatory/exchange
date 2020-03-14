from exchange.dal import f

from flask import Blueprint

s = Blueprint('s', __name__)


@s.route("/")
def func():
    f()
    return "1"
