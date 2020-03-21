import pytest
from exchange.custom_fields import (
    CustomField,
    DateTime,
    Decimal,
    Integer,
    OperationType,
    String,
)


def test_validate_emtpy():
    cf = CustomField(required=True)
    assert not cf.validate_empty()


def test_validate_empty_with_no_required():
    cf = CustomField()
    assert cf.validate_empty()


def test_validate_integer():
    i = Integer(required=True)
    assert not i.validate('a')


@pytest.fixture()
def required_decimal():
    return Decimal(required=True)


def test_validate_decimal(required_decimal):
    assert required_decimal.validate(1)


def test_validate_decimal_with_string_raises_error(required_decimal):
    assert not required_decimal.validate('1')


def test_validate_date_time():
    dt = DateTime(required=True)
    assert dt.validate('2016-06-06 11:22:33')


@pytest.fixture()
def operation_type():
    return OperationType(required=True)


def test_operation_type(operation_type):
    assert operation_type.validate('BUY')
    assert operation_type.validate('SELL')


def test_operation_type_with_invalid_arg(operation_type):
    assert not operation_type.validate('11:22:33 2016-06-06')


def test_empty_string_validation():
    assert not String(required=True).validate(None)
