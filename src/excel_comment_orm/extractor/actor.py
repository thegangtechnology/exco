import abc
from typing import Any, TypeVar, Type
from typing import Dict

T = TypeVar('T')


class Actor(abc.ABC):
    @classmethod
    def create(cls: Type[T], params: Dict[str, Any]) -> T:
        return cls(**params)
