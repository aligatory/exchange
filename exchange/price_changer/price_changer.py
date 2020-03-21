import random
from datetime import datetime
from decimal import Decimal
from time import sleep
from typing import NoReturn

from exchange.config import (
    MAX_DISPERSION_IN_PERCENTS,
    MIN_DISPERSION_IN_PERCENTS,
    PRICE_CHANGE_DELAY_SECONDS,
)
from exchange.data_base import Database, create_session
from exchange.models import Currency


def _get_new_random_price(current_price: Decimal) -> Decimal:
    percent: Decimal = Decimal(
        random.uniform(MIN_DISPERSION_IN_PERCENTS, MAX_DISPERSION_IN_PERCENTS)
    )
    sign = random.randint(0, 1)
    delta: Decimal = current_price / 100 * percent
    res: Decimal = (current_price - delta) if sign else (current_price + delta)
    return res


def start_value_changer_process() -> NoReturn:
    Database.create()
    while True:
        sleep(PRICE_CHANGE_DELAY_SECONDS)
        change_currencies()


def change_currencies() -> None:
    with create_session() as session:
        for currency in session.query(Currency).all():
            currency.selling_price = _get_new_random_price(currency.selling_price)
            currency.purchasing_price = _get_new_random_price(currency.purchasing_price)
            currency.last_change_time = datetime.now()
            session.add(currency)


def start_after_sleep() -> NoReturn:
    sleep(2)  # чтобы не было конфликта с главным потоком во время создания БД
    start_value_changer_process()
