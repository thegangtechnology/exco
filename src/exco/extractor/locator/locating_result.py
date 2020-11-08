from dataclasses import dataclass
from typing import Optional

from exco import CellLocation


@dataclass
class LocatingResult:
    location: Optional[CellLocation]
    is_ok: bool
    msg: str = ""
    exception: Optional[Exception] = None

    @classmethod
    def good(cls, location: CellLocation) -> 'LocatingResult':
        return LocatingResult(location=location, is_ok=True)

    @classmethod
    def bad(cls, msg: str, exception: Optional[Exception] = None) -> 'LocatingResult':
        return LocatingResult(location=None, is_ok=False, msg=msg, exception=exception)
