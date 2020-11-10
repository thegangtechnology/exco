from exco.exception import ParserSpecCreationException
from exco.extractor_spec.parser_spec import ParserSpec
import pytest


def test_parser_spec():
    spec = ParserSpec.from_dict({
        'parser': 'int',
        'params': {}
    })

    assert spec.name == 'int'
    assert spec.params == {}


def test_parser_spec_no_name():
    with pytest.raises(ParserSpecCreationException):
        ParserSpec.from_dict({
            'parserrr': 'int',
            'params': {}
        })


def test_parser_spec_no_param():
    spec = ParserSpec.from_dict({
        'parser': 'int',
    })
    assert spec.params == {}
