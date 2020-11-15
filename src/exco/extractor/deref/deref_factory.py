from typing import Dict, Type

from exco.extractor.base_factory import BaseFactory
from exco.extractor.deref.built_in.everything_deref import EverythingDeref
from exco.extractor.deref.built_in.no_deref import NoDeref
from exco.extractor.deref.deref import Deref
from exco.extractor_spec.deref_spec import DerefSpec


class DerefFactory(BaseFactory[Deref, DerefSpec]):
    def __init__(self, class_map: Dict[str, Type[Deref]]):
        super().__init__(class_map)

    @classmethod
    def suffix(cls):
        return 'Deref'

    @classmethod
    def default(cls) -> 'DerefFactory':
        return cls(cls.build_class_dict([
            EverythingDeref,
            NoDeref
        ]))
