from dataclasses import dataclass
from typing import Dict

from exco.cell_full_path import CellFullPath


@dataclass
class TableEndConditionParam:
    """Parameter to send to End Condition 's test function"""
    row_count: int
    """row count including this row"""
    cfps: Dict[str, CellFullPath]
    """dictionary from column key to cell full path"""
