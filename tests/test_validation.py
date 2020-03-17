from typing import Dict, Any

import pytest

from exchange.api.validation import validate_request_params
from exchange.exceptions import ValidationException


def test_validate_request_params():
    a_value: str = '1'
    b_value: str = 'a'
    res: Dict[str, Any] = validate_request_params(types=dict(a=int, b=str), current=dict(a=a_value, b=b_value))
    assert res.get('a') == 1
    assert res.get('b') == b_value


def test_validate_invalid_params_raises_error():
    a_value: str = 'a'
    with pytest.raises(ValidationException):
        res: Dict[str, Any] = validate_request_params(types=dict(a=int), current=dict(a=a_value))
