from dataclasses import dataclass

from exco.extractor.table_end_conditions.table_end_condition_param import TableEndConditionParam
from exco.extractor.table_end_conditions.table_end_condition_result import TableEndConditionResult
from exco.extractor.table_end_conditions.table_end_condition import TableEndCondition


@dataclass
class AllRowBlankTableEndCondition(TableEndCondition):

    def test(self, param: TableEndConditionParam) -> TableEndConditionResult:
        all_blanks = all(cfp.is_blank() for key, cfp in param.cfps.items())
        return TableEndConditionResult.good(
            should_terminate=all_blanks,
            is_inclusive=False
        )
