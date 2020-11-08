from typing import Type, Any, Dict

from exco.cell_full_path import CellFullPath
from exco.extractor.validator.built_in.value_validator import ValueValidator
from exco.extractor.validator.validation_result import ValidationResult
from exco.extractor.validator.validator import Validator


class IsNotBlankValidator(ValueValidator[str]):
    def validate_value(self, value: str) -> bool:
        return value == ''
