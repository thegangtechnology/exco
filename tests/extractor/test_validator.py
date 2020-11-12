from unittest.mock import patch

import pytest

from exco.extractor import Validator
from exco.extractor.validator.built_in.is_not_blank_validator import IsNotBlankValidator
from exco.extractor.validator.built_in.value_validator import ValueValidator
from exco.extractor.validator.validation_result import ValidationResult


def test_is_not_blank_validator():
    validator = IsNotBlankValidator()
    assert validator.validate('a') == ValidationResult.bad(
        msg=f'Fail a fail validation of {str(validator)}')
    assert validator.validate('') == ValidationResult.good()


@patch.multiple(ValueValidator, __abstractmethods__=set())
def test_value_validator_abstract():
    with pytest.raises(NotImplementedError):
        vv = ValueValidator()
        vv.validate_value("a")


@patch.multiple(Validator, __abstractmethods__=set())
def test_validator_abstract():
    with pytest.raises(NotImplementedError):
        vv = Validator()
        vv.validate(value="a")
