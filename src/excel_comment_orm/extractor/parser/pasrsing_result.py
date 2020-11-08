from dataclasses import dataclass
from typing import Generic, Optional, TypeVar

T = TypeVar('T')


@dataclass
class ParsingResult(Generic[T]):
    value: Optional[T]
    is_ok: bool
    msg: str = ""
    exception: Optional[Exception] = None

    def get_value(self, default: T) -> T:
        if self.is_ok:
            return self.value
        else:
            return default

    @classmethod
    def bad(cls, msg: str = "", exception: Optional[Exception] = None) -> 'ParsingResult':
        return ParsingResult(
            value=None, is_ok=False, msg=msg, exception=exception
        )

    @classmethod
    def good(cls, value: T, msg: str = "") -> 'ParsingResult':
        return ParsingResult(
            value=value, is_ok=True, msg=msg
        )
