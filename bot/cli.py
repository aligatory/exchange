import json
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from http import HTTPStatus
from time import sleep
from typing import NoReturn, Optional, Dict, Any, Tuple

import click

from bot.exceptions import BotException
from exchange.http_methods import HTTPMethod
from exchange.operation_type import OperationType
from requests import Response
import requests

@dataclass
class Currency:
    time: datetime
    purchasing_price: Decimal
    selling_price: Decimal

@click.command()
@click.option('-c', 'currency_id', help='Currency id', type=int)
@click.option('-p', 'profit', help='trades until profit percent', type=Decimal)
@click.option('-s', 'start_buy_amount', help='start buy amount', type=Decimal, required=True)
def start_bot(currency_id: int, profit: Decimal, start_buy_amount: Decimal):
    while True:
        sleep(2)
        print(datetime.now())


class Bot:
    BASE_URL: str = 'http://localhost:5000/'

    def __init__(self, currency_id: int, profit: Decimal, start_buy_amount: Decimal) -> None:
        self.currency_id = currency_id
        self.profit = profit
        self.start_buy_amount = start_buy_amount

    def start(self) -> NoReturn:
        user_id = self.register_user('crypto_investor')
        currency = self.get_currency_json(self.currency_id)
        response = self.buy(user_id, self.currency_id, self.start_buy_amount, currency.time)
        if response.status_code != HTTPStatus.CREATED and response.json()["error"] == 'currency price was change, ' \
                                                                                      'check new price':

    def buy(self, user_id: int, currency_id: int, amount: Decimal, time: datetime) -> Response:
        return self.make_operation(user_id, currency_id, amount, OperationType.BUY, time)

    def make_operation(self, user_id: int, currency_id: int, amount: Decimal, operation: OperationType,
                       time) -> Response:
        return self.make_request(Bot.BASE_URL + f'users/{user_id}/currencies/', HTTPMethod.POST, data=dict(
            currency_id=currency_id,
            amount=str(amount), operation=operation.name, time=datetime.strftime(time, '%Y-%m-%d %H:%M:%S')))

    def register_user(self, login: str) -> int:
        response: Response = Bot.make_request(Bot.BASE_URL + 'users/', HTTPMethod.POST, dict(login=login))
        if response.status_code != HTTPStatus.CREATED:
            raise BotException(response.json()['message'])
        return response.json()['id']

    @staticmethod
    def make_request(url: str, method: HTTPMethod, data: Optional[Dict[str, Any]] = None) -> Response:
        j = None
        if data is not None:
            j = json.dumps(data)
        if method == HTTPMethod.GET:
            return requests.get(url, j)
        if method == HTTPMethod.POST:
            return requests.post(url, j)
        raise TypeError('Invalid type or not implemented')

    def get_currency(self, currency_id: int) -> Currency:
        response: Response = Bot.make_request(Bot.BASE_URL + f'currencies/{currency_id}/', HTTPMethod.GET)
        j = response.json()
        return Currency(purchasing_price=j["purchasing_price"],selling_price=j["selling_price"],time=j['time'])



# b = Bot(1, Decimal('1.0'), Decimal('1.0'))
# b.register_user('t')
# b.make_operation(1, 1, b.start_buy_amount, OperationType.BUY)
