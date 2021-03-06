from datetime import datetime
from decimal import Decimal

import pytest
from exchange.app import create_app
from exchange.dal.users_dal import UsersDAL
from exchange.data_base import Base, create_session, engine
from exchange.models import Currency


@pytest.fixture()
def app():
    app = create_app(test_call=True)
    app.config['TESTING'] = True
    return app


@pytest.fixture()
def client(app):
    with app.test_client() as client:
        return client


@pytest.fixture()
def user_login():
    return 'test'


@pytest.fixture()
def currency_params():
    return 'test', Decimal('1'), Decimal('1')


# понимаю, что тут надо исользовать usefixture, но т.к. эта фикстура, то тут такое не работает
# вроде как pytest этого не умеет, есть какой-то вариант как это исправить?
@pytest.fixture(scope='function', autouse=True)
def _init_db():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture()
def _add_currency(currency_params):
    with create_session() as session:
        currency = Currency(
            name=currency_params[0],
            purchasing_price=currency_params[1],
            selling_price=currency_params[2],
            modified_at=datetime.now(),
        )
        session.add(currency)


@pytest.fixture()
def _add_user(user_login):
    UsersDAL.add_user(user_login)
