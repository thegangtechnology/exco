from dataclasses import dataclass

from exco.extractor.table_end_conditions.table_end_condition_param import TableEndConditionParam
from exco.extractor.table_end_conditions.table_end_condition_result import TableEndConditionResult
from exco.extractor.table_end_conditions.table_end_condition import TableEndCondition


@dataclass
class MaxRowTableEndCondition(TableEndCondition):
    """
    End Condition when maximum number of row is reached.
    """
    n: int
    inclusive: bool = True

    def test(self, param: TableEndConditionParam) -> TableEndConditionResult:
        """Return True if the the row number is greater than or equal to
        self.n.
        Args:
            param (TableEndConditionParam):

        Returns:
            TableEndConditionResult
        """
        max_row_reached = param.row_count >= self.n
        return TableEndConditionResult.good(
            should_terminate=max_row_reached,
            is_inclusive=self.inclusive
        )
