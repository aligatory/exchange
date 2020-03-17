<<<<<<< HEAD
from typing import Any, Dict

import pytest
=======
from typing import Dict, Any

import pytest

>>>>>>> f7ef0e1bb6257452ae30c6f4c9f47c1a1006ebea
from exchange.api.validation import validate_request_params
from exchange.exceptions import ValidationException


def test_validate_request_params():
    a_value: str = '1'
    b_value: str = 'a'
<<<<<<< HEAD
    res: Dict[str, Any] = validate_request_params(
        types=dict(a=int, b=str), current=dict(a=a_value, b=b_value)
    )
=======
    res: Dict[str, Any] = validate_request_params(types=dict(a=int, b=str), current=dict(a=a_value, b=b_value))
>>>>>>> f7ef0e1bb6257452ae30c6f4c9f47c1a1006ebea
    assert res.get('a') == 1
    assert res.get('b') == b_value


def test_validate_invalid_params_raises_error():
    a_value: str = 'a'
    with pytest.raises(ValidationException):
<<<<<<< HEAD
        validate_request_params(types=dict(a=int), current=dict(a=a_value))
=======
        res: Dict[str, Any] = validate_request_params(types=dict(a=int), current=dict(a=a_value))
>>>>>>> f7ef0e1bb6257452ae30c6f4c9f47c1a1006ebea
