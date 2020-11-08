import abc
from typing import Generic

from excel_comment_orm.cell_full_path import CellFullPath
from excel_comment_orm.extractor.actor import Actor
from excel_comment_orm.extractor.processor import T
from excel_comment_orm.extractor.validator.validation_result import ValidationResult


class Validator(Actor, abc.ABC, Generic[T]):
    @abc.abstractmethod
    def validate(self, value: T) -> ValidationResult:
        raise NotImplementedError()
