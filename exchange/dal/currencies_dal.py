from copy import deepcopy
from decimal import Decimal
from typing import List

from exchange.api.serialization import (
    AbstractSerialize,
    CurrencyOutputFields,
    Serializer,
)
from exchange.data_base import create_session
from exchange.exceptions import CurrenciesDALException
from exchange.models import Currency


class CurrenciesDAL:
    @staticmethod
    def get_currencies() -> List[AbstractSerialize]:
        currencies: List[AbstractSerialize] = []
        with create_session() as session:
            for currency in session.query(Currency):
                currencies.append(Serializer.serialize(currency, CurrencyOutputFields))
        return currencies

    @staticmethod
    def add_currency(
        name: str, selling_price: Decimal, purchasing_price: Decimal
    ) -> AbstractSerialize:
        with create_session() as session:
            if (
                session.query(Currency).filter(Currency.name == name).first()
                is not None
            ):
                raise CurrenciesDALException('Currency with this name already exists')
            currency = Currency(
                name=name,
                selling_price=selling_price,
                purchasing_price=purchasing_price,
            )
            session.add(currency)
            session.flush()
            currency_copy = deepcopy(currency)

        return Serializer.serialize(currency_copy, CurrencyOutputFields)
