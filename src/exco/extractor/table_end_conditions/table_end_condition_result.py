from dataclasses import dataclass
from typing import Optional


@dataclass
class TableEndConditionResult:
    should_terminate: bool
    is_inclusive: bool
    is_ok: bool
    msg: str = ''
    exception: Optional[Exception] = None

    @property
    def is_exclusive(self):
        return not self.is_inclusive

    @classmethod
    def good(cls, should_terminate: bool, is_inclusive: bool) -> 'TableEndConditionResult':
        return TableEndConditionResult(
            should_terminate=should_terminate,
            is_inclusive=is_inclusive,
            is_ok=True
        )

    @classmethod
    def bad(cls, msg: str = '', exception: Optional[Exception] = None) -> 'TableEndConditionResult':
        return TableEndConditionResult(
            should_terminate=True,
            is_inclusive=False,
            is_ok=False,
            msg=msg,
            exception=exception
        )
