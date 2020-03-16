import pytest
from exchange.app import create_app
from exchange.data_base import Database


@pytest.fixture()
def app():
    app = create_app()
    app.config['TESTING'] = True
    return app


@pytest.fixture()
def client(app):
    with app.test_client() as client:
        return client


@pytest.fixture(scope='session')
def _create_db():
    Database.create()


# понимаю, что тут надо исользовать usefixture, но т.к. эта фикстура, то тут такое не работает
# вроде как pytest этого не умеет, есть какой-то вариант как это исправить?
@pytest.fixture(scope='function', autouse=True)
def _init_db(_create_db):
    Database.base.metadata.create_all(Database.engine)
    yield
    Database.base.metadata.drop_all(Database.engine)
