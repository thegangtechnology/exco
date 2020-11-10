from dataclasses import dataclass

from exco.extractor.table_end_conditions.table_end_condition_param import TableEndConditionParam
from exco.extractor.table_end_conditions.table_end_condition_result import TableEndConditionResult
from exco.extractor.table_end_conditions.table_end_condition import TableEndCondition


@dataclass
class AllBlankTableEndCondition(TableEndCondition):
    """
    End Condition when all cell in the row is blank.
    """

    def test(self, param: TableEndConditionParam) -> TableEndConditionResult:
        """ Return True if all cells in this table row is blank.

        Args:
            param (TableEndConditionParam):

        Returns:
            TableEndConditionResult
        """
        all_blanks = all(cfp.is_blank() for key, cfp in param.cfps.items())
        return TableEndConditionResult.good(
            should_terminate=all_blanks,
            is_inclusive=False
        )
