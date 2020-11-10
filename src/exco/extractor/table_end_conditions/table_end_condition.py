import abc

from exco.extractor.actor import Actor
from exco.extractor.table_end_conditions.table_end_condition_param import TableEndConditionParam
from exco.extractor.table_end_conditions.table_end_condition_result import TableEndConditionResult


class TableEndCondition(Actor, abc.ABC):
    """Abstract class for TableEndCondition"""

    @abc.abstractmethod
    def test(self, param: TableEndConditionParam) -> TableEndConditionResult:
        """abstract method on how each implementation decides where the table should end"""
        raise NotImplementedError()
