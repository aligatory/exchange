import random
from datetime import datetime
from decimal import Decimal
from time import sleep
from typing import NoReturn

from exchange.config import settings
from exchange.data_base import create_session
from exchange.models import Currency


def _get_new_random_price(current_price: Decimal) -> Decimal:
    percent: Decimal = Decimal(
        random.uniform(
            settings.min_dispersion_in_percents, settings.max_dispersion_in_percents
        )
    )
    sign = random.randint(0, 1)
    delta: Decimal = current_price / 100 * percent
    res: Decimal = (current_price - delta) if sign else (current_price + delta)
    return res


def start_value_changer_process() -> NoReturn:
    while True:
        sleep(settings.price_change_delay_seconds)
        change_currencies()


def change_currencies() -> None:
    with create_session() as session:
        for currency in session.query(Currency).all():
            price = _get_new_random_price(
                (currency.selling_price + currency.purchasing_price) / 2
            )
            currency.selling_price = price * Decimal('0.975')
            currency.purchasing_price = price * Decimal('1.025')
            currency.last_change_time = datetime.now()
            session.add(currency)


def start_after_sleep() -> NoReturn:
    start_value_changer_process()
