from typing import Type, Any, Dict

from excel_comment_orm.cell_full_path import CellFullPath
from excel_comment_orm.extractor.validator.validation_result import ValidationResult
from excel_comment_orm.extractor.validator.validator import Validator


class IsNotBlankValidator(Validator[str]):
    def validate(self, value: str) -> ValidationResult:
        if value == '':
            return ValidationResult.bad('Value is Blank')
        else:
            return ValidationResult.good()
