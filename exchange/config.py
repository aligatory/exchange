from dataclasses import dataclass
from decimal import Decimal
from typing import List

START_MONEY = Decimal('1000')
PRICE_CHANGE_DELAY_SECONDS: int = 10
MAX_DISPERSION_IN_PERCENTS: int = 10
MIN_DISPERSION_IN_PERCENTS: int = 1


@dataclass
class Currency:
    name: str
    selling_price: Decimal
    purchasing_price: Decimal


DEFAULT_CURRENCIES: List[Currency] = [
    Currency('bitcoin', Decimal('0.9'), Decimal('1.1')),
    Currency('etherium', Decimal('1.9'), Decimal('2.1')),
    Currency('litecoin', Decimal('2.9'), Decimal('3.1')),
    Currency('monero', Decimal('3.9'), Decimal('4.1')),
    Currency('xrp', Decimal('4.9'), Decimal('5.1')),
]
