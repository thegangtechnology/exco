from typing import Dict, Type

from exco import LocatorSpec
from exco.extractor.base_factory import BaseFactory
from exco.extractor.locator.built_in.at_comment_cell_locator import AtCommentCellLocator
from exco.extractor.locator.built_in.right_of_locator import RightOfLocator
from exco.extractor.locator.built_in.right_of_regex_locator import RightOfRegexLocator
from exco.extractor.locator.locator import Locator


class LocatorFactory(BaseFactory[Locator, LocatorSpec]):
    def __init__(self, class_map: Dict[str, Type[Locator]]):
        super().__init__(class_map)

    @classmethod
    def suffix(cls):
        return 'Locator'

    @classmethod
    def default(cls) -> 'LocatorFactory':
        return cls(cls.build_class_dict([
            AtCommentCellLocator,
            RightOfLocator,
            RightOfRegexLocator
        ]))
