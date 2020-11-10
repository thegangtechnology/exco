from dataclasses import dataclass
from typing import Dict

from exco.cell_full_path import CellFullPath


@dataclass
class TableEndConditionParam:
    row_count: int  # include this row
    cfps: Dict[str, CellFullPath]
