from typing import Any, Dict

import pytest
from exchange.exceptions import ValidationException
from exchange.validation import RequestParam, validate_request_params


def test_validate_request_params():
    a_value: str = '1'
    b_value: str = 'a'
    res: Dict[str, Any] = validate_request_params(
        request_params=dict(a=RequestParam(int, True), b=RequestParam(str, True)),
        current=dict(a=a_value, b=b_value),
    )
    assert res.get('a') == 1
    assert res.get('b') == b_value


def test_validate_invalid_params_raises_error():
    a_value: str = 'a'
    with pytest.raises(ValidationException):
        validate_request_params(
            request_params=dict(a=RequestParam(int, True)), current=dict(a=a_value)
        )


def test_validate_req_params_without_required_param():
    with pytest.raises(ValidationException):
        validate_request_params(dict(a=RequestParam(int, True)), dict())
