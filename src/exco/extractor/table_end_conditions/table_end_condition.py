import abc

from exco.extractor.table_end_conditions.table_end_condition_param import TableEndConditionParam
from exco.extractor.table_end_conditions.table_end_condition_result import TableEndConditionResult


class TableEndCondition(abc.ABC):
    @abc.abstractmethod
    def test(self, param: TableEndConditionParam) -> TableEndConditionResult:
        raise NotImplementedError()
