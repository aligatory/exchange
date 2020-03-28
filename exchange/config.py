from dataclasses import dataclass
from decimal import Decimal
from typing import List

from pydantic import BaseSettings


@dataclass
class Currency:
    name: str
    selling_price: Decimal
    purchasing_price: Decimal


class Settings(BaseSettings):
    start_money: Decimal = Decimal('1000')
    price_change_delay_seconds: int = 10
    max_dispersion_in_percents: int = 10
    min_dispersion_in_percents: int = 1
    default_currencies: List[Currency] = [
        Currency('bitcoin', Decimal('0.975'), Decimal('1.025')),
        Currency('etherium', Decimal('1.95'), Decimal('2.05')),
        Currency('litecoin', Decimal('2.925'), Decimal('3.075')),
        Currency('monero', Decimal('3.9'), Decimal('4.1')),
        Currency('xrp', Decimal('4.875'), Decimal('5.125')),
    ]


settings = Settings()
