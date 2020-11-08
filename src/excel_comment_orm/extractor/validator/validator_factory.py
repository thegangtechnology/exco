from typing import Dict, Type

from excel_comment_orm import ValidatorSpec
from excel_comment_orm.extractor.base_factory import BaseFactory
from excel_comment_orm.extractor.validator.built_in.is_not_blank_validator import IsNotBlankValidator
from excel_comment_orm.extractor.validator.validator import Validator


class ValidatorFactory(BaseFactory[Validator, ValidatorSpec]):
    def __init__(self, class_map: Dict[str, Type[Validator]]):
        super().__init__(class_map)

    @classmethod
    def suffix(self):
        return 'Validator'

    @classmethod
    def default(cls) -> 'ValidatorFactory':
        return cls(cls.build_class_dict([
            IsNotBlankValidator
        ]))
