from decimal import Decimal

import pytest
from exchange.config import START_MONEY
from exchange.dal.users_dal import UsersDAL
from exchange.data_base import create_session
from exchange.exceptions import UsersDALException
from exchange.models import User


@pytest.fixture()
def user_login():
    return 'test'


def test_add_user_returns_valid(user_login):
    res = UsersDAL.add_user(user_login)
    assert res.money == Decimal(START_MONEY)
    assert res.login == user_login


@pytest.fixture()
def _with_add_user_to_db(user_login):
    UsersDAL.add_user(user_login)


@pytest.mark.usefixtures('_with_add_user_to_db')
def test_add_user_to_db(user_login):
    with create_session() as session:
        user_from_db: User = session.query(User).filter(User.id == 1).first()
        assert user_from_db.login == user_login
        assert user_from_db.money == START_MONEY


@pytest.mark.usefixtures('_with_add_user_to_db')
def test_add_user_to_db_second_time(user_login):
    with pytest.raises(UsersDALException):
        UsersDAL.add_user(user_login)
