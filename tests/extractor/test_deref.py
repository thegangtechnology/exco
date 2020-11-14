from os.path import join, dirname

import openpyxl

from exco import ExcelProcessorFactory
from exco.deref import deref_text


def test_deref_text():
    sheet_name = "TestSheet"
    workbook = openpyxl.load_workbook(join(dirname(__file__), '../../sample/test/deref/deref_template.xlsx'))
    text = "<<A2>> and <<B2>>"
    result = deref_text(sheet_name=sheet_name, workbook=workbook, text=text)
    assert result == "sum_val and 20"

    text = "{{A2}} and <<B2>> and <<a1>>"
    result = deref_text(sheet_name=sheet_name, workbook=workbook, text=text)
    assert result == "{{A2}} and 20 and <<a1>>"


def test_deref_failed():
    sheet_name = "TestSheet"
    workbook = openpyxl.load_workbook(join(dirname(__file__), '../../sample/test/deref/deref_template.xlsx'))
    text = "<<ZZZ000>>"
    result = deref_text(sheet_name=sheet_name, workbook=workbook, text=text)
    assert result == text


def test_deref_fallback():
    fname = join(dirname(__file__), '../../sample/test/deref/deref_template.xlsx')
    processor = ExcelProcessorFactory.default().create_from_template_excel(fname)

    another_file = join(dirname(__file__),
                        '../../sample/test/deref/deref_fallback.xlsx')
    result = processor.process_excel(another_file)
    assert result.to_dict() == {'sum_val': '500'}
