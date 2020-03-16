import json
from typing import Any, Dict, Optional, TypeVar

from exchange.api.custom_fields import CustomField
from exchange.exceptions import ValidationException
from flask_restplus import Model
from flask_restplus.fields import Raw


def validate_json(payload: Optional[Dict[str, Any]], api_model: Model) -> None:
    if payload is None:
        raise ValidationException('Request do not contains body')
    for key in api_model:
        if api_model[key].required and key not in payload:
            raise ValidationException(f'Required field {key} missing')
    for key in payload:
        field = api_model[key]
        value = payload[key]
        validate_data(value, field, key)


T = TypeVar('T')


def validate_data(value: T, field: Raw, key: str) -> None:
    if isinstance(field, CustomField) and hasattr(field, 'validate'):
        if not field.validate(value):
            raise ValidationException(f'Validation of {key} field failed')


def get_dict_from_json(data: bytes) -> Dict[str, Any]:
    try:
        return json.loads(data)
    except BaseException:
        raise ValidationException('Request body is not json')
