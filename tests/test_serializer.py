import pytest
from exchange.models import User
from exchange.serialization import Serializer


def test_serializer_with_invalid_target_class():
    with pytest.raises(TypeError):
        Serializer.serialize(User, int)
