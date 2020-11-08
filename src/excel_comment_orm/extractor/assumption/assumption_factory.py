from typing import Dict, Type

from excel_comment_orm import AssumptionSpec
from excel_comment_orm.extractor.assumption.assumption import Assumption
from excel_comment_orm.extractor.assumption.built_in.left_cell_match_assumption import LeftCellMatchAssumption
from excel_comment_orm.extractor.base_factory import BaseFactory


class AssumptionFactory(BaseFactory[Assumption, AssumptionSpec]):
    def __init__(self, class_map: Dict[str, Type[Assumption]]):
        super().__init__(class_map)

    @classmethod
    def suffix(self):
        return 'Assumption'

    @classmethod
    def default(cls) -> 'AssumptionFactory':
        return cls(cls.build_class_dict([
            LeftCellMatchAssumption
        ]))
