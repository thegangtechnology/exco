from typing import Type, Any, Dict

from exco.cell_full_path import CellFullPath
from exco.extractor.validator.validation_result import ValidationResult
from exco.extractor.validator.validator import Validator


class IsNotBlankValidator(Validator[str]):
    def validate(self, value: str) -> ValidationResult:
        if value == '':
            return ValidationResult.bad('Value is Blank')
        else:
            return ValidationResult.good()
