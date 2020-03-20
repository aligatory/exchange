from typing import List, TypeVar

from exchange.exceptions import PaginationError

T = TypeVar('T')


class MyPagination:
    @staticmethod
    def get_pagination(objects: List[T], page: int, size: int) -> List[T]:
        start_index: int = 0
        if page < 1 or size < 1 or page * size >= len(objects) + size:
            raise PaginationError('invalid page or size params')
        if page > 1:
            start_index = (page - 1) * size
        end_index: int = start_index + size - 1
        length = len(objects)
        if end_index >= length:
            end_index = length - 1
        res: List[T] = []
        for i in range(start_index, end_index + 1):
            res.append(objects[i])
        return res
