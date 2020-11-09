from typing import Dict, Type

from exco import AssumptionSpec
from exco.extractor.assumption.assumption import Assumption
from exco.extractor.assumption.built_in.left_cell_match_assumption import LeftCellMatchAssumption
from exco.extractor.base_factory import BaseFactory


class AssumptionFactory(BaseFactory[Assumption, AssumptionSpec]):
    def __init__(self, class_map: Dict[str, Type[Assumption]]):
        super().__init__(class_map)

    @classmethod
    def suffix(cls):
        return 'Assumption'

    @classmethod
    def default(cls) -> 'AssumptionFactory':
        return cls(cls.build_class_dict([
            LeftCellMatchAssumption
        ]))
