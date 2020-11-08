import abc
from typing import Generic, TypeVar

from exco.extractor.actor import Actor
from exco.extractor.validator.validation_result import ValidationResult

T = TypeVar('T')


class Validator(Actor, abc.ABC, Generic[T]):
    @abc.abstractmethod
    def validate(self, value: T) -> ValidationResult:
        raise NotImplementedError()
