from dataclasses import dataclass
from typing import Optional


@dataclass
class ValidationResult:
    is_ok: bool
    msg: str = ""
    exception: Optional[Exception] = None

    @classmethod
    def good(cls) -> 'ValidationResult':
        return ValidationResult(is_ok=True)

    @classmethod
    def bad(cls, msg: str = "", exception: Optional[Exception] = None):
        return ValidationResult(
            is_ok=False,
            msg=msg,
            exception=exception
        )
