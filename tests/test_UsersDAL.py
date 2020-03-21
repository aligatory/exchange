from datetime import datetime, timedelta
from decimal import Decimal
from typing import List

import pytest
from exchange.config import START_MONEY
from exchange.dal.users_dal import UsersDAL
from exchange.data_base import create_session
from exchange.exceptions import UsersDALException
from exchange.models import User, UserCurrency
from exchange.operation_type import OperationType
from exchange.serialization import UserCurrencyFields


def test_add_user_returns_valid(user_login):
    res = UsersDAL.add_user(user_login)
    assert res.money == Decimal(START_MONEY)
    assert res.login == user_login


@pytest.mark.usefixtures('_add_user')
def test_add_user_to_db(user_login):
    with create_session() as session:
        user_from_db: User = session.query(User).filter(User.id == 1).first()
        assert user_from_db.login == user_login
        assert user_from_db.money == START_MONEY


@pytest.mark.usefixtures('_add_user')
def test_add_user_to_db_second_time(user_login):
    with pytest.raises(UsersDALException):
        UsersDAL.add_user(user_login)


@pytest.mark.usefixtures('_add_currency')
@pytest.mark.usefixtures('_add_user')
def test_buy_currency():
    user_id = 1
    currency_id = 1
    amount = Decimal('1')
    user_currency: UserCurrencyFields = UsersDAL.make_operation_with_currency(
        user_id, currency_id, OperationType.BUY, amount, datetime.now()
    )
    assert user_currency.id == currency_id
    assert user_currency.user_id == user_id
    assert user_currency.amount == amount
    with create_session() as session:
        user = session.query(User).filter(User.id == 1).first()
        assert user.money == Decimal('999')


@pytest.mark.usefixtures('_add_currency')
@pytest.mark.usefixtures('_add_user')
def test_buy_with_insufficient_funds_raise_error():
    with pytest.raises(UsersDALException):
        UsersDAL.make_operation_with_currency(
            1, 1, OperationType.BUY, Decimal('1001'), datetime.now()
        )


@pytest.mark.usefixtures('_add_currency')
@pytest.mark.usefixtures('_add_user')
def test_sell_currency():
    user_id = 1
    currency_id = 1
    amount = Decimal('1')
    UsersDAL.make_operation_with_currency(
        user_id, currency_id, OperationType.BUY, amount, datetime.now()
    )
    user_currency: UserCurrencyFields = UsersDAL.make_operation_with_currency(
        user_id, currency_id, OperationType.SELL, amount, datetime.now()
    )
    assert user_currency.amount == Decimal('0')
    with create_session() as session:
        user = session.query(User).filter(User.id == user_id).first()
        assert user.money == Decimal('1000')
        assert session.query(UserCurrency).filter(UserCurrency.id == 1).first() is None


@pytest.mark.usefixtures('_add_currency')
@pytest.mark.usefixtures('_add_user')
def test_sell_more_than_have():
    user_id = 1
    currency_id = 1
    amount = Decimal('1')
    UsersDAL.make_operation_with_currency(
        user_id, currency_id, OperationType.BUY, amount, datetime.now()
    )
    with pytest.raises(UsersDALException):
        UsersDAL.make_operation_with_currency(
            user_id, currency_id, OperationType.SELL, Decimal('2'), datetime.now()
        )


@pytest.mark.usefixtures('_add_currency')
@pytest.mark.usefixtures('_add_user')
def test_get_user_currencies():
    UsersDAL.make_operation_with_currency(
        1, 1, OperationType.BUY, Decimal('1'), datetime.now()
    )
    currencies: List[UserCurrencyFields] = UsersDAL.get_user_currencies(1)
    assert len(currencies) == 1
    assert currencies[0].amount == Decimal('1')


def test_get_user_currencies_with_invalid_user_id():
    with pytest.raises(UsersDALException):
        UsersDAL.get_user_currencies(228)


@pytest.mark.usefixtures('_add_currency')
@pytest.mark.usefixtures('_add_user')
def test_buy_currency_with_old_price_known():
    with pytest.raises(UsersDALException):
        time = datetime.now() - timedelta(seconds=20)
        UsersDAL.make_operation_with_currency(
            1, 1, OperationType.BUY, Decimal('1.0'), time
        )


@pytest.mark.usefixtures('_add_currency')
@pytest.mark.usefixtures('_add_user')
def test_buy_currency_with_too_early_time():
    with pytest.raises(UsersDALException):
        time = datetime.now() + timedelta(seconds=1000)
        UsersDAL.make_operation_with_currency(
            1, 1, OperationType.BUY, Decimal('1.0'), time
        )


@pytest.mark.usefixtures('_add_currency')
@pytest.mark.usefixtures('_add_user')
def test_sell_nonexistent_currency():
    with pytest.raises(UsersDALException):
        UsersDAL.make_operation_with_currency(
            1, 1, OperationType.SELL, Decimal('1.0'), datetime.now()
        )
