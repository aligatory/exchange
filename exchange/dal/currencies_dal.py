from datetime import datetime
from decimal import Decimal
from typing import List

from exchange.data_base import create_session
from exchange.exceptions import CurrenciesDALException
from exchange.models import Currency
from exchange.serialization import AbstractSerialize, CurrencyOutputFields, Serializer


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
            if selling_price <= 0 or purchasing_price <= 0:
                raise CurrenciesDALException(
                    'Selling or purchasing price less or equal to zero'
                )
            if (
                session.query(Currency).filter(Currency.name == name).first()
                is not None
            ):
                raise CurrenciesDALException('Currency with this name already exists')
            currency = Currency(
                name=name,
                selling_price=selling_price,
                purchasing_price=purchasing_price,
                last_change_time=datetime.now(),
            )
            session.add(currency)
            session.flush()
            return Serializer.serialize(currency, CurrencyOutputFields)

    @staticmethod
    def get_currency_by_id(currency_id: int) -> AbstractSerialize:
        with create_session() as session:
            res: Currency = session.query(Currency).filter(
                Currency.id == currency_id
            ).first()
            if res is None:
                raise CurrenciesDALException('Currency not exists')
            return Serializer.serialize(res, CurrencyOutputFields)
