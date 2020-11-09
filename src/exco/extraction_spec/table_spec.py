from dataclasses import dataclass, field
from enum import Enum
from typing import Dict

from exco.extraction_spec.locator_spec import LocatorSpec
from exco.extraction_spec.type import SpecParam


class TableDirection(Enum):
    DOWNWARD = 'downward'
    RIGHTWARD = 'rightward'


Offset = int


@dataclass
class TableSpec:
    key: str
    locator: LocatorSpec
    columns: Dict[Offset, APVSpec]  # offset -> APVSpec
    end_conditions: Dict[str, SpecParam] = field(default_factory=lambda: {"all_blank": True, "max_row": 500})
    direction: TableDirection = TableDirection.DOWNWARD
