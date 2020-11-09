from typing import Dict, Type

from exco import ValidatorSpec
from exco.extractor.base_factory import BaseFactory
from exco.extractor.validator.built_in.between_validator import BetweenValidator
from exco.extractor.validator.built_in.is_not_blank_validator import IsNotBlankValidator
from exco.extractor.validator.validator import Validator


class ValidatorFactory(BaseFactory[Validator, ValidatorSpec]):
    def __init__(self, class_map: Dict[str, Type[Validator]]):
        super().__init__(class_map)

    @classmethod
    def suffix(cls):
        return 'Validator'

    @classmethod
    def default(cls) -> 'ValidatorFactory':
        return cls(cls.build_class_dict([
            IsNotBlankValidator,
            BetweenValidator
        ]))
