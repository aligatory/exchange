import pytest
from build.lib.exchange.data_base import create_session
from exchange.config import DEFAULT_CURRENCIES
from exchange.db_actions import add_default_currencies, clear_db
from exchange.models import Currency


def test_add_default_currencies():
    add_default_currencies()
    with create_session() as session:
        currencies = session.query(Currency).all()
        assert len(currencies) == len(DEFAULT_CURRENCIES)


def test_clear_db():
    add_default_currencies()
    clear_db()
    with create_session() as session:
        with pytest.raises(BaseException):
            session.query(Currency).all()
