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
    Currency('bitcoin', Decimal('1.1'), Decimal('0.9')),
    Currency('etherium', Decimal('2.1'), Decimal('1.9')),
    Currency('litecoin', Decimal('3.1'), Decimal('2.9')),
    Currency('monero', Decimal('4.1'), Decimal('3.9')),
    Currency('xrp', Decimal('5.1'), Decimal('4.9')),
]
