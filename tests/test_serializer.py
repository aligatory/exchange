import pytest
from exchange.serialization import serialize


def test_serializer_with_invalid_target_class():
    with pytest.raises(TypeError):
        serialize(object())
