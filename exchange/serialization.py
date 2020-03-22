from abc import ABC
from datetime import datetime
from decimal import Decimal
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


class Serializer:
    T1 = TypeVar('T1', bound=Type[AbstractSerialize])
    T2 = TypeVar('T2', bound=Base)

    @staticmethod
    def serialize(db_object: T2, clazz: T1) -> AbstractSerialize:
        if clazz is CurrencyOutputFields:
            return CurrencyOutputFields(db_object)
        if clazz is UserOutputFields:
            return UserOutputFields(db_object)
        if clazz is UserCurrencyFields:
            return UserCurrencyFields(db_object)
        if clazz is UserOperationFields:
            return UserOperationFields(db_object)
        raise TypeError()
