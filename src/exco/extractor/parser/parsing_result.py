from dataclasses import dataclass
from typing import Generic, Optional, TypeVar

T = TypeVar('T')


@dataclass
class ParsingResult(Generic[T]):
    value: T
    is_ok: bool
    msg: str = ""
    exception: Optional[Exception] = None

    def get_value(self) -> T:
        return self.value

    @classmethod
    def bad(cls, fallback: T, msg: str = "",
            exception: Optional[Exception] = None) -> 'ParsingResult[T]':
        return ParsingResult(
            value=fallback, is_ok=False, msg=msg, exception=exception
        )

    @classmethod
    def good(cls, value: T, msg: str = "") -> 'ParsingResult[T]':
        return ParsingResult(
            value=value, is_ok=True, msg=msg
        )
