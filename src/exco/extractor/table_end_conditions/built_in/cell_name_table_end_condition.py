from dataclasses import dataclass

from exco.extractor.table_end_conditions.table_end_condition_param import TableEndConditionParam
from exco.extractor.table_end_conditions.table_end_condition_result import TableEndConditionResult
from exco.extractor.table_end_conditions.table_end_condition import TableEndCondition


@dataclass
class CellNameTableEndCondition(TableEndCondition):
    end_label: str

    def test(self, param: TableEndConditionParam) -> TableEndConditionResult:
        for _, cfp in param.cfps.items():
            is_cell_name = cfp.cell.value == self.end_label
            if is_cell_name:
                break
        return TableEndConditionResult.good(
            should_terminate=is_cell_name,
            is_inclusive=False
        )


