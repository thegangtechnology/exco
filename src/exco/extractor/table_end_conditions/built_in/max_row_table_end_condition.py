from dataclasses import dataclass

from exco.extractor.table_end_conditions.table_end_condition_param import TableEndConditionParam
from exco.extractor.table_end_conditions.table_end_condition_result import TableEndConditionResult
from exco.extractor.table_end_conditions.table_end_condition import TableEndCondition


@dataclass
class MaxRowTableEndCondition(TableEndCondition):
    n: int
    inclusive: bool = True

    def test(self, param: TableEndConditionParam) -> TableEndConditionResult:
        max_row_reached = param.row_count >= self.n
        return TableEndConditionResult.good(
            should_terminate=max_row_reached,
            is_inclusive=self.inclusive
        )
