from datetime import datetime
from decimal import Decimal
from typing import List

from exchange.data_base import create_session
from exchange.exceptions import CurrenciesDALException
from exchange.models import Currency, CurrencyHistory
from exchange.serialization import AbstractSerialize, serialize


class CurrenciesDAL:
    @staticmethod
    def get_currencies() -> List[AbstractSerialize]:
        currencies: List[AbstractSerialize] = []
        with create_session() as session:
            for currency in session.query(Currency):
                currencies.append(serialize(currency))
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
                modified_at=datetime.now(),
            )
            session.add(currency)
            session.flush()
            currency_history = CurrencyHistory(
                currency_id=currency.id,
                time=currency.modified_at,
                purchasing_price=purchasing_price,
                selling_price=selling_price,
            )
            session.add(currency_history)
            return serialize(currency)

    @staticmethod
    def get_currency_by_id(currency_id: int) -> AbstractSerialize:
        with create_session() as session:
            res: Currency = session.query(Currency).filter(
                Currency.id == currency_id
            ).first()
            if res is None:
                raise CurrenciesDALException('Currency not exists')
            return serialize(res)

    @staticmethod
    def get_currency_history(currency_id: int) -> List[AbstractSerialize]:
        with create_session() as session:
            currency = (
                session.query(Currency).filter(Currency.id == currency_id).first()
            )
            if currency is None:
                raise CurrenciesDALException('Currency not exists')
            res: List[AbstractSerialize] = []
            for currency_history in (
                session.query(CurrencyHistory)
                .filter(CurrencyHistory.currency_id == currency_id)
                .all()
            ):
                res.append(serialize(currency_history))
            return res
