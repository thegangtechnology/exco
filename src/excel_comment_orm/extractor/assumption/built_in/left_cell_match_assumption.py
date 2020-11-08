from dataclasses import dataclass
from typing import Dict, Any

from excel_comment_orm.cell_full_path import CellFullPath
from excel_comment_orm.extractor.assumption.assumption import Assumption
from excel_comment_orm.extractor.assumption.assumption_result import AssumptionResult


@dataclass
class LeftCellMatchAssumption(Assumption):
    label: str

    def assume(self, cfp: CellFullPath) -> AssumptionResult:
        cond = cfp.shift(col=-1).cell.value == self.label
        if cond:
            return AssumptionResult.good()
        else:
            return AssumptionResult.bad(f'Cell to the left of {cfp.cell.coordinate} does not match {self.label}')
