import pytest

from exco.exception import ParsingFailException
from exco.extractor.parser.built_in.float_parser import FloatParser
from exco.extractor.parser.built_in.int_parser import IntParser
from exco.extractor.parser.built_in.string_parser import StringParser


def test_parser_parse_float():
    assert FloatParser().parse_value('3.0') == float(3.0)

    with pytest.raises(ParsingFailException):
        FloatParser().parse_value('a')


def test_parser_parse_int():
    assert IntParser().parse_value('3') == int(3.0)

    with pytest.raises(ParsingFailException):
        IntParser().parse_value('3.2')


def test_parser_parse_str():
    assert StringParser().parse_value('a') == str('a')
