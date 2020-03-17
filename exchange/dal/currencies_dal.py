<<<<<<< HEAD
from copy import deepcopy
=======
>>>>>>> f7ef0e1bb6257452ae30c6f4c9f47c1a1006ebea
from decimal import Decimal
from typing import List
from copy import deepcopy

from sqlalchemy.orm import Session

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
<<<<<<< HEAD
        name: str, selling_price: Decimal, purchasing_price: Decimal
=======
            name: str, selling_price: Decimal, purchasing_price: Decimal
>>>>>>> f7ef0e1bb6257452ae30c6f4c9f47c1a1006ebea
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
