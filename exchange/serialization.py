from abc import ABC
from datetime import datetime
from decimal import Decimal
from functools import singledispatch
from typing import Type, TypeVar

from exchange.models import Base, Currency, Operation, User, UserCurrency


class AbstractSerialize(ABC):
    pass


class CurrencyOutputFields(AbstractSerialize):
    def __init__(self, db_object: Currency):
        self.id: int = db_object.id
        self.name: str = db_object.name
        self.purchasing_price: Decimal = db_object.purchasing_price
        self.selling_price: Decimal = db_object.selling_price
        self.time: str = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')


class UserOutputFields(AbstractSerialize):
    def __init__(self, db_object: User):
        self.id: int = db_object.id
        self.login: str = db_object.login
        self.money: Decimal = db_object.money


class UserCurrencyFields(AbstractSerialize):
    def __init__(self, db_object: UserCurrency):
        self.id = db_object.id
        self.user_id = db_object.user_id
        self.currency_id = db_object.currency_id
        self.amount = db_object.amount


class UserOperationFields(AbstractSerialize):
    def __init__(self, db_object: Operation):
        self.id: int = db_object.id
        self.operation_type: str = db_object.operation_type.name
        self.currency_id = db_object.currency_id
        self.amount = db_object.amount
        self.time = datetime.strftime(db_object.time, '%Y-%m-%d %H:%M:%S')


T1 = TypeVar('T1', bound=Type[AbstractSerialize])
T2 = TypeVar('T2', bound=Base)


@singledispatch
def serialize(db_object: T2) -> AbstractSerialize:
    raise TypeError()


@serialize.register
def _(db_object: Currency) -> AbstractSerialize:
    return CurrencyOutputFields(db_object)


@serialize.register  # type: ignore
def _(db_object: User) -> AbstractSerialize:
    return UserOutputFields(db_object)


@serialize.register  # type: ignore
def _(db_object: UserCurrency) -> AbstractSerialize:
    return UserCurrencyFields(db_object)


@serialize.register  # type: ignore
def _(db_object: Operation) -> AbstractSerialize:
    return UserOperationFields(db_object)
