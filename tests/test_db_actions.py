import pytest
from exchange.config import settings
from exchange.data_base import create_session
from exchange.db_actions import add_default_currencies, clear_db
from exchange.models import Currency


def test_add_default_currencies() -> None:
    add_default_currencies()
    with create_session() as session:
        currencies = session.query(Currency).all()
        assert len(currencies) == len(settings.default_currencies)


def test_clear_db() -> None:
    add_default_currencies()
    clear_db()
    with create_session() as session:
        with pytest.raises(BaseException):
            session.query(Currency).all()
