from datetime import datetime, timedelta
from decimal import Decimal
from http import HTTPStatus

import pytest

#
from exchange.bot.cli import Bot, Currency, User
from exchange.bot.exceptions import BotException
from exchange.config import START_MONEY
from exchange.http_methods import HTTPMethod


@pytest.fixture()
def requests_get_mock(mocker):
    return mocker.patch('requests.get')


@pytest.fixture()
def requests_post_mock(mocker):
    return mocker.patch('requests.post')


@pytest.fixture()
def user(login):
    return User(login, 1, Decimal('999'))


@pytest.fixture()
def currency():
    return Currency('test', datetime.now(), Decimal('1.025'), Decimal('0.975'))


def test_get_currency(requests_get_mock):
    name = 'bitcoin'
    purchasing_price = '1.22'
    selling_price = '1.23'
    requests_get_mock.return_value.json.return_value = {
        'name': name,
        'purchasing_price': purchasing_price,
        'selling_price': selling_price,
        'time': datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'),
    }
    currency = Bot.get_currency(1)
    assert currency.purchasing_price == Decimal(purchasing_price)
    assert currency.selling_price == Decimal(selling_price)
    assert currency.name == name


def test_add_user(login, requests_post_mock):
    requests_post_mock.return_value.json.return_value = dict(
        id='1', login=login, money=str(START_MONEY)
    )
    user = Bot.register_user(login)
    assert user.money == START_MONEY
    assert user.login == login
    assert user.id == 1


@pytest.fixture(scope='session')
def login():
    return 'login'


@pytest.fixture()
def _bot_mock_register_user(mocker, user):
    mocker.patch.object(Bot, 'register_user')
    Bot.register_user.return_value = user


@pytest.fixture()
def _bot_patch_get_currency(mocker):
    mocker.patch.object(Bot, 'get_currency')


@pytest.fixture()
def _bot_mock_get_currency(currency, _bot_patch_get_currency):
    Bot.get_currency.return_value = currency


@pytest.fixture()
def _bot_mock_get_multiple_currencies_currency_growing(_bot_patch_get_currency):
    time1 = datetime.now()
    time2 = time1 + timedelta(seconds=2)
    name = 'test'
    Bot.get_currency.side_effect = [
        Currency(name, time1, Decimal('1.025'), Decimal('0.975')),
        Currency(name, time2, Decimal('1.5'), Decimal('1.35')),
    ]


@pytest.fixture()
def _bot_mock_get_multiple_currencies_currency_falls(_bot_patch_get_currency):
    time1 = datetime.now()
    time2 = time1 + timedelta(seconds=2)
    name = 'test'
    Bot.get_currency.side_effect = [
        Currency(name, time2, Decimal('1.5'), Decimal('1.35')),
        Currency(name, time1, Decimal('1.025'), Decimal('0.975')),
    ]


@pytest.fixture()
def bot():
    return Bot(1, Decimal('1.0'), Decimal('1.0'))


@pytest.mark.usefixtures('_bot_mock_register_user')
@pytest.mark.usefixtures('_bot_mock_get_currency')
def test_first_buy(mocker, bot):
    mocker.patch.object(Bot, 'buy')
    assert bot.first_buy().name == 'test'


def test_bot_make_request_with_invalid_http_method():
    with pytest.raises(TypeError):
        Bot.make_request('google.com', None)


def test_bot_make_request_when_it_get_error_in_response(requests_get_mock):
    requests_get_mock.return_value.status_code = HTTPStatus.BAD_REQUEST
    requests_get_mock.return_value.json.return_value = {'message': 'my_error'}
    with pytest.raises(BotException):
        Bot.make_request('google.com', HTTPMethod.GET)


@pytest.mark.usefixtures('_bot_mock_register_user')
@pytest.mark.usefixtures('_bot_mock_get_currency')
def test_first_buy_when_time_was_change(mocker, bot):
    mocker.patch.object(Bot, 'buy')
    Bot.buy.side_effect = [
        BotException('currency price was change, check new price'),
        None,
    ]
    assert bot.first_buy().name == 'test'


@pytest.mark.usefixtures('_bot_mock_register_user')
@pytest.mark.usefixtures('_bot_mock_get_multiple_currencies_currency_growing')
def test_bot_monitoring(mocker, bot):
    mocker.patch.object(Bot, 'buy')
    mocker.patch.object(bot, 'sell')
    bot.start()
    assert bot.bot_finished


@pytest.mark.usefixtures('_bot_mock_get_multiple_currencies_currency_falls')
@pytest.mark.usefixtures('_bot_mock_register_user')
def test_bot_monitoring_with_currency_falls(mocker, bot):
    mocker.patch.object(Bot, 'buy')
    mocker.patch.object(bot, 'sell')
    with pytest.raises(StopIteration):  # валюты из фикстуры две, они заканчиваются
        bot.start()  # бот ждет дальше, но дальше валют нет, падает StopIteration
        # не знаю как можно лучше понять, что беск цикл не завершился
