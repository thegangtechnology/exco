from os.path import join, dirname

import openpyxl
import pytest

from exco import ExcelProcessorFactory
from exco.deref import DerefCell
from exco.extractor.parser.built_in.int_parser import IntParser


@pytest.fixture
def dc_1() -> DerefCell:
    sheet_name = "TestSheet"
    workbook = openpyxl.load_workbook(join(dirname(__file__), '../../sample/test/deref/deref_template.xlsx'))
    dc = DerefCell(sheet_name=sheet_name,
                   workbook=workbook)
    return dc


def test_deref_text(dc_1: DerefCell):
    text = "<<A2>> and <<B2>>"
    result = dc_1.deref_text(text)
    assert result == "sum_val and 20"

    text = "{{A2}} and <<B2>> and <<a1>>"
    result = dc_1.deref_text(text)
    assert result == "{{A2}} and 20 and <<a1>>"

    text = "<<B2>>"
    result = dc_1.deref_text(text, parser=IntParser())
    assert result == 20


def test_deref_failed(dc_1: DerefCell):
    text = "<<ZZZ000>>"
    result = dc_1.deref_text(text)
    assert result == text


def test_deref_key_and_fallback():
    fname = join(dirname(__file__), '../../sample/test/deref/deref_template.xlsx')
    processor = ExcelProcessorFactory.default().create_from_template_excel(fname)

    another_file = join(dirname(__file__),
                        '../../sample/test/deref/deref_test_1.xlsx')
    result = processor.process_excel(another_file)
    assert result.to_dict() == {'sum_val': 500, 'awesome_wealth': 200}


def test_deref_locator():
    fname = join(dirname(__file__), '../../sample/test/deref/deref_template_2.xlsx')
    processor = ExcelProcessorFactory.default().create_from_template_excel(fname)

    another_file = join(dirname(__file__),
                        '../../sample/test/deref/deref_test_2.xlsx')
    result = processor.process_excel(another_file)
    assert result.to_dict() == {'sum_val': 150}
