from dataclasses import dataclass
from typing import Optional


@dataclass
class AssumptionResult:
    is_ok: bool
    msg: str = ""
    exception: Optional[Exception] = None

    @classmethod
    def good(cls):
        return AssumptionResult(is_ok=True)

    @classmethod
    def bad(cls, msg: str = '', exception: Optional[Exception] = None):
        return AssumptionResult(is_ok=False, msg=msg, exception=exception)
