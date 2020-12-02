from os.path import join, dirname
from unittest.mock import patch

import pytest

from exco import ExcoTemplate, ExcelProcessorFactory
from exco.exception import ActorCreationFailException
from exco.extractor_spec.parser_spec import ParserSpec
from exco.extractor.base_factory import BaseFactory
from exco.extractor.parser.built_in.int_parser import IntParser
from exco.extractor.parser.built_in.string_parser import StringParser
from exco.extractor.parser.parser_factory import ParserFactory


def test_simple():
    fname = join(dirname(__file__), '../../sample/test/simple.xlsx')
    template = ExcoTemplate.from_excel(fname)
    spec = template.to_raw_excel_processor_spec()
    fac = ExcelProcessorFactory.default()
    processor = fac.create_from_spec(spec)

    another_file = join(dirname(__file__),
                        '../../sample/test/simple_no_comment.xlsx')
    result = processor.process_excel(another_file)
    assert result.to_dict() == {'random_value': 'hello',
                                'some_int': 99, 'some_str': '99'}


def test_simple_short_version():
    fname = join(dirname(__file__), '../../sample/test/simple.xlsx')
    processor = ExcelProcessorFactory.default().create_from_template_excel(fname)

    another_file = join(dirname(__file__),
                        '../../sample/test/simple_no_comment.xlsx')
    result = processor.process_excel(another_file)
    assert result.to_dict() == {'random_value': 'hello',
                                'some_int': 99, 'some_str': '99'}


@patch.multiple(BaseFactory, __abstractmethods__=set())
def test_base_factory_abstract():
    with pytest.raises(NotImplementedError):
        bf = BaseFactory(class_map={})
        bf.suffix()


def test_factory_register_all():
    pf = ParserFactory(class_map={})
    pf.register_all([IntParser, StringParser])
    assert pf.available_keys() == ['int', 'string']


def test_failed_create_spec():
    pf = ParserFactory(class_map={})
    pf.register_all([IntParser, StringParser])

    pf.class_map['something'] = 1

    with pytest.raises(ActorCreationFailException):
        pf.create_from_spec(ParserSpec(name='myvar'))

    with pytest.raises(ActorCreationFailException):
        pf.create_from_spec(ParserSpec(name='something'))
