import abc
from typing import Generic, TypeVar

from exco.extractor.validator.validator import Validator
from exco.extractor.validator.validation_result import ValidationResult

T = TypeVar('T')


class ValueValidator(Generic[T], Validator[T], abc.ABC):
    @abc.abstractmethod
    def validate_value(self, value: T) -> bool:
        raise NotImplementedError()

    def validate(self, value: T) -> ValidationResult:
        if self.validate_value(value):
            return ValidationResult.good()
        else:
            return ValidationResult.bad(msg=f"Fail {value} fail validation of {self}")
