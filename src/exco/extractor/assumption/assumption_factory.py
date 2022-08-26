from typing import Dict, Type, Optional

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
    def default(cls, extras: Optional[Dict[str, Type[Assumption]]] = None) -> 'AssumptionFactory':
        defaults = cls.build_class_dict([
            LeftCellMatchAssumption
        ])
        extras = {} if extras is None else extras
        return cls({**defaults, **extras})
