from dataclasses import dataclass

from exco.extractor.table_end_conditions.table_end_condition_param import TableEndConditionParam
from exco.extractor.table_end_conditions.table_end_condition_result import TableEndConditionResult
from exco.extractor.table_end_conditions.table_end_condition import TableEndCondition


@dataclass
class CellValueTableEndCondition(TableEndCondition):
    cell_value: str

    def test(self, param: TableEndConditionParam) -> TableEndConditionResult:
        matching_cell_value = self._check_matching_cell_value(param)
        return TableEndConditionResult.good(
            should_terminate=matching_cell_value,
            is_inclusive=False
        )

    def _check_matching_cell_value(self, param: TableEndConditionParam) -> bool:
        for _, cfp in param.cfps.items():
            matching_cell_value = cfp.cell.value == self.cell_value
            if matching_cell_value:
                break
        return matching_cell_value
