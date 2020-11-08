import abc
from typing import Dict
from typing import Any, TypeVar, Type

from excel_comment_orm.cell_full_path import CellFullPath

T = TypeVar('T')


class Actor(abc.ABC):
    @classmethod
    def create(cls: Type[T], params: Dict[str, Any]) -> T:
        return cls(**params)
