import json
from typing import Any, Dict, Optional, Type, TypeVar

from exchange.api.custom_fields import CustomField
from exchange.exceptions import AuthError, ValidationException
from flask_restplus import Model
from flask_restplus.fields import Raw
from werkzeug.datastructures import Authorization


def validate_json(payload: Dict[str, Any], api_model: Model) -> None:
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


class ValidatedRequest:
    def __init__(
        self,
        json_data: Optional[Dict[str, Any]] = None,
        auth: Optional[Authorization] = None,
    ):
        self._json = json_data
        self._auth = auth

    def get_json(self) -> Dict[str, Any]:
        if self._json is None:
            raise ValueError()
        return self._json

    def get_auth(self) -> Authorization:
        if self._auth is None:
            raise ValueError()
        return self._auth


def validate_auth(auth: Optional[Authorization]) -> Authorization:
    if auth is None:
        raise AuthError('Auth error')
    return auth


def validate_json_and_auth(
    data: Optional[bytes], data_fields: Model,
) -> Dict[str, Any]:
    if data is None:
        raise ValidationException('Request body not contains json')
    input_json = get_dict_from_json(data)
    validate_json(input_json, data_fields)
    return input_json


def validate_auth_user_name(auth: Authorization) -> str:
    if auth.username is None or not isinstance(auth.username, str):
        raise ValidationException('Auth error')
    return auth.username


def validate_path_parameter(value: Optional[str]) -> int:
    if value is None or not value.isdigit():
        raise ValidationException('path parameter not a number')
    return int(value)


def validate_request_params(
    types: Dict[str, Type[Any]], current: Dict[str, Any]
) -> Dict[str, Any]:
    if len(types) != len(current):
        raise ValidationException('Invalid parameters size')
    res: Dict[str, Any] = {}
    for key, t in types.items():
        try:
            value: Any = current[key]
            res[key] = t(value)
        except BaseException:
            raise ValidationException(f'{key} invalid type or not expected')
    return res
