from os.path import join, dirname

import openpyxl

from exco.deref import deref_text


def test_deref_text():
    sheet_name = "TestSheet"
    workbook = openpyxl.load_workbook(join(dirname(__file__), '../../sample/test/deref/deref_template.xlsx'))
    text = "<<A2>> and <<B2>>"
    result = deref_text(sheet_name=sheet_name, workbook=workbook, text=text)
    assert result == "sum_val and 20"
