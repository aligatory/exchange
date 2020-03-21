import json
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, Optional, Type, TypeVar

from exchange.custom_fields import CustomField, DateTime
from exchange.custom_fields import OperationType as OTField
from exchange.exceptions import ValidationException
from exchange.operation_type import OperationType
from flask_restplus import Model
from flask_restplus.fields import Raw

T = TypeVar('T')


def _validate_data(value: T, field: Raw, key: str) -> None:
    if isinstance(field, CustomField) and hasattr(field, 'validate'):
        if not field.validate(value):
            raise ValidationException(f'Validation of {key} field failed')


def _validate_json(payload: Dict[str, Any], api_model: Model) -> None:
    for key in api_model:
        if api_model[key].required and key not in payload:
            raise ValidationException(f'Required field {key} missing')
    for key in payload:
        field = api_model[key]
        value = payload[key]
        _validate_data(value, field, key)
        if isinstance(field, DateTime):
            payload[key] = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        if isinstance(field, OTField):
            payload[key] = OperationType[value]


def get_dict_from_json(data: bytes) -> Dict[str, Any]:
    try:
        return json.loads(data, parse_float=Decimal)
    except BaseException:
        raise ValidationException('Request body is not json')


def validate_request_json(data: Optional[bytes], data_fields: Model,) -> Dict[str, Any]:
    if data is None:
        raise ValidationException('Request body not contains json')
    input_json = get_dict_from_json(data)
    _validate_json(input_json, data_fields)
    return input_json


def validate_path_parameter(value: Optional[str]) -> int:
    if value is None or not value.isdigit():
        raise ValidationException('path parameter not a number')
    return int(value)


@dataclass
class RequestParam:
    ttype: Type[Any]
    required: bool = False


def validate_request_params(
    request_params: Dict[str, RequestParam], current: Dict[str, Any]
) -> Dict[str, Any]:
    if len(request_params) != len(current) and all(
        map(lambda t: t.required, request_params.values())
    ):
        raise ValidationException('Invalid parameters size')
    res: Dict[str, Any] = {}
    for key, param in request_params.items():
        try:
            value: Any = current.get(key)
            if value is None and not param.required:
                continue
            if param.ttype is OperationType:
                res[key] = OperationType[value]
            else:
                res[key] = param.ttype(value)
        except BaseException:
            raise ValidationException(f'{key} invalid type or not expected')
    return res
