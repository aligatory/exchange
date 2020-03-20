
import pytest
from exchange.dal.currencies_dal import CurrenciesDAL
from exchange.data_base import create_session
from exchange.exceptions import CurrenciesDALException
from exchange.models import Currency
from exchange.serialization import CurrencyOutputFields


@pytest.fixture()
def _add_currency(currency_params):
    CurrenciesDAL.add_currency(*currency_params)


def test_add_currency(currency_params):
    currency: CurrencyOutputFields = CurrenciesDAL.add_currency(*currency_params)
    assert currency.id == 1
    with create_session() as session:
        currency = session.query(Currency).filter(Currency.id == 1).first()
        assert currency.selling_price == currency_params[1]
        assert currency.purchasing_price == currency_params[2]


@pytest.mark.usefixtures('_add_currency')
def test_add_currency_that_already_exists(currency_params):
    with pytest.raises(CurrenciesDALException):
        CurrenciesDAL.add_currency(*currency_params)


@pytest.mark.usefixtures('_add_currency')
def test_get_currencies():
    res = CurrenciesDAL.get_currencies()
    assert len(res) == 1
    assert res[0].id == 1


@pytest.mark.usefixtures('_add_currency')
def test_get_currency_by_id():
    res = CurrenciesDAL.get_currency_by_id(1)
    assert res.id == 1


@pytest.mark.usefixtures('_add_currency')
def test_get_currency_with_invalid_id():
    with pytest.raises(CurrenciesDALException):
        CurrenciesDAL.get_currency_by_id(2)
