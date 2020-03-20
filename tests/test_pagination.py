# type: ignore
from typing import List, Optional

import pytest
from exchange.dal.pagination import MyPagination


@pytest.mark.parametrize(('size', 'page', 'expected_size'), [(15, 1, 15), (8, 2, 7)])
def test_pagination(size: int, page: int, expected_size: int):
    count_of_operations: int = 15
    objects: List[Optional[int]] = [None] * count_of_operations
    for i in range(count_of_operations):
        objects[i] = i
    res: List[int] = MyPagination.get_pagination(objects, page=page, size=size)
    assert len(res) == expected_size
