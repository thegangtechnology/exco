from os.path import join, dirname

import exco
import openpyxl
from exco import CellLocation
from exco.dereferator import Dereferator


def test_deref():
    template = join(dirname(__file__), '../sample/test/simple_deref.xlsx')
    processor = exco.from_excel(template)
    data = join(dirname(__file__), '../sample/test/simple_deref_to_extract.xlsx')
    result = processor.process_excel(data)
    assert result.to_dict() == {
        'deref_key': 12,
        'world': 34
    }


def test_deref_recursive():
    wb = openpyxl.Workbook()
    sheet = wb.active
    for i in range(10):
        sheet.cell(i + 1, 1).value = i + 1
    dereferator = Dereferator.template_to_spec(workbook=wb, anchor=CellLocation(
        sheet_name=sheet.title,
        coordinate='A1'
    ))
    assert dereferator.deref(['a', '<<A2>>']) == ['a', 2]
