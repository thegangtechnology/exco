from exco.extractor.validator.built_in.value_validator import ValueValidator


class IsNotBlankValidator(ValueValidator[str]):
    def validate_value(self, value: str) -> bool:
        return value == ''
