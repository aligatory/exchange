from abc import abstractmethod
from datetime import datetime
from decimal import Decimal as D
from typing import Any, Optional, TypeVar

from exchange.exceptions import DateTimeParseException
from exchange.operation_type import OperationType as OT
from flask_restplus.fields import Raw


class CustomField(Raw):
    def __init__(self, *args: Any, **kwargs: Any):
        super(CustomField, self).__init__(*args, **kwargs)

    def validate_empty(self) -> bool:
        if self.required:
            return False
        return True

    T = TypeVar('T')

    @abstractmethod
    def validate(self, value: T) -> bool:
        pass


class String(CustomField):
    __schema_example__ = 'string'

    def validate(self, value: CustomField.T) -> bool:
        if not value:
            return self.validate_empty()
        return isinstance(value, str)


class DateTime(CustomField):
    __schema_format__ = 'date-time'
    __schema_example__ = '2016-06-06 11:22:33'
    dt_format = '%Y-%m-%d %H:%M:%S'

    def from_str(self, value: str) -> Optional[datetime]:
        try:
            return None if not value else datetime.strptime(value, self.dt_format)
        except BaseException:
            raise DateTimeParseException()

    def validate(self, value: CustomField.T) -> bool:
        if not value or not isinstance(value, str):
            return self.validate_empty()
        try:
            self.from_str(value)
        except DateTimeParseException:
            return False
        return True


class Decimal(CustomField):
    __schema_type__ = 'number'
    __schema_format__ = 'decimal'
    __schema_example__ = 0.0

    def validate(self, value: CustomField.T) -> bool:
        if value is None:
            return self.validate_empty()
        if not isinstance(value, D) and not isinstance(value, int):
            return False
        return True


class OperationType(CustomField):
    __schema_type__ = 'string'
    __schema_example__ = 'BUY'

    def validate(self, value: CustomField.T) -> bool:
        if not isinstance(value, str):
            return False
        try:
            return bool(OT[value])
        except KeyError:
            return False


class Integer(CustomField):
    __schema_type__ = 'integer'
    __schema_format__ = 'int'
    __schema_example__ = 0
    T = TypeVar('T')

    def validate(self, value: T) -> bool:
        if value is None:
            return self.validate_empty()
        if not isinstance(value, int):
            return False
        return True
