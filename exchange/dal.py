from exchange.data_base import create_session
from exchange.models import User


def f():
    with create_session() as session:
        u = User(login='evgeny111', money=-1)
        session.add(u)
