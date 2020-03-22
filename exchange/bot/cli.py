import json
from dataclasses import dataclass
from datetime import datetime
from decimal import ROUND_FLOOR, Decimal
from http import HTTPStatus
from threading import Thread
from time import sleep
from typing import Any, Dict, Optional

import click
import requests
from exchange.bot.exceptions import BotException
from exchange.http_methods import HTTPMethod
from exchange.operation_type import OperationType
from requests import Response


def get_amount(money: Decimal, price: Decimal) -> Decimal:
    return (money / price).quantize(Decimal('1.00000'), ROUND_FLOOR)


@dataclass
class Currency:
    name: str
    time: datetime
    purchasing_price: Decimal
    selling_price: Decimal


@dataclass
class User:
    login: str
    id: int
    money: Decimal


class Bot:
    BASE_URL: str = 'http://localhost:5000/'

    def __init__(
        self, currency_id: int, profit_percent: Decimal, money: Decimal
    ) -> None:
        self.currency_id = currency_id
        self.profit_percent = profit_percent
        self.money: Decimal = money
        self.potential_money: Optional[Decimal] = None
        self.amount: Optional[Decimal] = None
        self.user_id: Optional[int] = None
        self.currency_name: Optional[str] = None
        self.bot_finished: bool = False

    def start(self) -> None:
        self.first_buy()
        self.monitor_market()

    def monitor_market(self) -> None:
        amount: Decimal = self.amount  # type: ignore

        while True:
            sleep(1)
            currency = self.get_currency(self.currency_id)
            self.potential_money = currency.selling_price * amount
            price = self.money + self.money / 100 * self.profit_percent
            if (
                amount * currency.selling_price >= price
            ):  # user_id и amount устанавливаются в
                try:  # first_buy
                    self.sell(
                        self.user_id, self.currency_id, self.amount, currency.time  # type: ignore
                    )
                    self.bot_finished = True
                    break
                except BotException as e:
                    if e == 'currency price was change, check new price':
                        continue

    def first_buy(self) -> Currency:
        self.user_id = self.register_user('crypto_investor').id
        currency_at_the_time_of_purchase = self.get_currency(self.currency_id)
        self.amount = get_amount(
            self.money, currency_at_the_time_of_purchase.purchasing_price
        )
        self.currency_name = currency_at_the_time_of_purchase.name
        try:
            self.buy(
                self.user_id,
                self.currency_id,
                self.amount,
                currency_at_the_time_of_purchase.time,
            )
        except BotException as e:
            if str(e) == 'currency price was change, check new price':
                currency_at_the_time_of_purchase = self.get_currency(self.currency_id)
                amount = get_amount(
                    self.money, currency_at_the_time_of_purchase.purchasing_price
                )
                self.buy(
                    self.user_id,
                    self.currency_id,
                    amount,
                    currency_at_the_time_of_purchase.time,
                )
            else:
                raise
        self.potential_money = (
            currency_at_the_time_of_purchase.selling_price * self.amount
        )
        return currency_at_the_time_of_purchase

    @staticmethod
    def sell(
        user_id: int, currency_id: int, amount: Decimal, time: datetime
    ) -> Response:
        return Bot.make_operation(
            user_id, currency_id, amount, OperationType.SELL, time
        )

    @staticmethod
    def buy(
        user_id: int, currency_id: int, amount: Decimal, time: datetime
    ) -> Response:
        return Bot.make_operation(user_id, currency_id, amount, OperationType.BUY, time)

    @staticmethod
    def make_operation(
        user_id: int,
        currency_id: int,
        amount: Decimal,
        operation: OperationType,
        time: datetime,
    ) -> Response:
        return Bot.make_request(
            Bot.BASE_URL + f'users/{user_id}/currencies/',
            HTTPMethod.POST,
            data=dict(
                currency_id=currency_id,
                amount=str(amount),
                operation=operation.name,
                time=datetime.strftime(time, '%Y-%m-%d %H:%M:%S'),
            ),
        )

    @staticmethod
    def register_user(login: str) -> User:
        response: Response = Bot.make_request(
            Bot.BASE_URL + 'users/', HTTPMethod.POST, dict(login=login)
        )
        j = response.json()
        return User(j['login'], int(j['id']), Decimal(j['money']))

    @staticmethod
    def make_request(
        url: str, method: HTTPMethod, data: Optional[Dict[str, Any]] = None
    ) -> Response:
        j = None
        if data is not None:
            j = json.dumps(data)
        if method == HTTPMethod.GET:
            response = requests.get(url, j)
        elif method == HTTPMethod.POST:
            response = requests.post(url, j)
        else:
            raise TypeError('Invalid type or not implemented')
        a = response.status_code
        if a == HTTPStatus.BAD_REQUEST:
            raise BotException(response.json()['message'])
        return response

    @staticmethod
    def get_currency(currency_id: int) -> Currency:
        response: Response = Bot.make_request(
            Bot.BASE_URL + f'currencies/{currency_id}/', HTTPMethod.GET
        )
        j = response.json()
        return Currency(
            purchasing_price=Decimal(j['purchasing_price']),
            selling_price=Decimal(j['selling_price']),
            time=datetime.strptime(j['time'], '%Y-%m-%d %H:%M:%S'),
            name=j['name'],
        )


def show_info(bot: Bot) -> None:
    while not bot.bot_finished:
        sleep(5)
        print(f'u have {bot.potential_money} of {bot.currency_name}')  # type: ignore
        print(f'potential money : {round(bot.potential_money, 2)}')  # type: ignore
        # first_buy после 5 секунд amount точно
        # не будет None, так считает ее при запуске
        # аналогично с potential_money
    print(
        f'Bot sold currency {bot.amount} of {bot.currency_name} and get {bot.potential_money}'
    )


@click.command()
@click.option('-c', 'currency_id', help='Currency id', type=int, required=True)
@click.option(
    '-p', 'profit', help='trades until profit percent', type=Decimal, required=True
)
@click.option(
    '-s', 'start_buy_amount', help='start buy amount', type=Decimal, required=True
)
def start_bot(currency_id: int, profit: Decimal, start_buy_amount: Decimal) -> None:
    bot = Bot(currency_id, profit, start_buy_amount)
    Thread(target=show_info, args=[bot]).start()
    bot.start()
