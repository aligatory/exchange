from abc import ABC
from datetime import datetime
from decimal import Decimal
from typing import Type, TypeVar

from exchange.models import Base, Currency, User


class AbstractSerialize(ABC):
    pass

class CurrencyOutputFields(AbstractSerialize):
    def __init__(self, db_object: Currency):
        self.id: int = db_object.id
        self.name: str = db_object.name
        self.purchasing_price: Decimal = db_object.purchasing_price
        self.selling_price: Decimal = db_object.selling_price
        self.time: datetime = datetime.now()


class UserOutputFields(AbstractSerialize):
    def __init__(self, db_object: User):
        self.id: int = db_object.id
        self.login: str = db_object.login
        self.money: Decimal = db_object.money


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
