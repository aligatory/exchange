from abc import ABC
from datetime import datetime
from typing import Type, TypeVar

from exchange.models import Base, Currency, User


class AbstractSerialize(ABC):
    pass


class CurrencyOutputFields(AbstractSerialize):
    def __init__(self, db_object: Currency):
        self.name = db_object.name
        self.purchasing_price = db_object.purchasing_price
        self.selling_price = db_object.selling_price
        self.time = datetime.now()


class UserOutputFields(AbstractSerialize):
    def __init__(self, db_object: User):
        self.login = db_object.login
        self.money = db_object.money


class Serializer:
    T1 = TypeVar('T1', bound=Type[AbstractSerialize])
    T2 = TypeVar('T2', bound=Base)

    @staticmethod
    def serialize(db_object: T2, clazz: T1) -> AbstractSerialize:
        if clazz is CurrencyOutputFields:
            return CurrencyOutputFields(db_object)
        if clazz is UserOutputFields:
            return UserOutputFields(db_object)
        raise TypeError()
