from dataclasses import dataclass

from exco.extractor.validator.built_in.value_validator import ValueValidator


@dataclass
class BetweenValidator(ValueValidator[float]):
    low: float
    high: float

    def validate_value(self, v: float):
        return self.low <= v <= self.high
