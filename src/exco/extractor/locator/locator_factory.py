from typing import Dict, Type, Optional

from exco import LocatorSpec
from exco.extractor.base_factory import BaseFactory
from exco.extractor.locator.built_in.at_comment_cell_locator import AtCommentCellLocator
from exco.extractor.locator.built_in.right_of_locator import RightOfLocator
from exco.extractor.locator.built_in.right_of_regex_locator import RightOfRegexLocator
from exco.extractor.locator.built_in.below_of_locator import BelowOfLocator
from exco.extractor.locator.built_in.below_of_regex_locator import BelowOfRegexLocator
from exco.extractor.locator.built_in.within_locator import WithinLocator
from exco.extractor.locator.built_in.search_right_of_locator import SearchRightOfLocator
from exco.extractor.locator.built_in.search_below_of_locator import SearchBelowOfLocator
from exco.extractor.locator.locator import Locator


class LocatorFactory(BaseFactory[Locator, LocatorSpec]):
    def __init__(self, class_map: Dict[str, Type[Locator]]):
        super().__init__(class_map)

    @classmethod
    def suffix(cls):
        return 'Locator'

    @classmethod
    def default(cls, extras: Optional[Dict[str, Type[Locator]]] = None) -> 'LocatorFactory':
        defaults = cls.build_class_dict([
            AtCommentCellLocator,
            RightOfLocator,
            RightOfRegexLocator,
            BelowOfLocator,
            BelowOfRegexLocator,
            WithinLocator,
            SearchRightOfLocator,
            SearchBelowOfLocator
        ])
        extras = {} if extras is None else extras
        return cls({**defaults, **extras})
