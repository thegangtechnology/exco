from typing import Dict, Type

from exco.extractor.base_factory import BaseFactory
from exco.extractor.table_end_conditions.built_in.all_row_blank_table_end_condition import AllRowBlankTableEndCondition
from exco.extractor.table_end_conditions.built_in.max_row_table_end_condition import MaxRowTableEndCondition
from exco.extractor.table_end_conditions.table_end_condition import TableEndCondition
from exco.extractor_spec.table_extraction_spec import TableEndConditionSpec


class TableEndConditionFactory(BaseFactory[TableEndCondition, TableEndConditionSpec]):
    def __init__(self, class_map: Dict[str, Type[TableEndCondition]]):
        super().__init__(class_map)

    @classmethod
    def suffix(cls):
        return 'TableEndCondition'

    @classmethod
    def default(cls) -> 'TableEndConditionFactory':
        return cls(cls.build_class_dict([
            AllRowBlankTableEndCondition,
            MaxRowTableEndCondition
        ]))
