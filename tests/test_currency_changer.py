from decimal import Decimal

from exchange.data_base import create_session
from exchange.models import Currency
from exchange.price_changer.price_changer import change_currencies


def test_change_currencies():
    price = Decimal('1')
    with create_session() as session:
        currency = Currency(name='test', purchasing_price=price, selling_price=price)
        session.add(currency)
    change_currencies()
    with create_session() as session:
        currency = session.query(Currency).filter(Currency.id == 1).first()
        assert currency.purchasing_price != price
        assert currency.selling_price != price
