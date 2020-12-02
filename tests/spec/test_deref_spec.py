from exco import CellLocation
from exco.dereferator import Dereferator
from openpyxl import Workbook
import pytest


@pytest.fixture
def workbook() -> Workbook:
    wb = Workbook()
    sheet = wb.active
    sheet.title = 'SHEET1'
    sheet['A1'] = 1
    sheet['A2'] = 'hello'
    return wb


def test_deref_post_spec(workbook):
    dereferator = Dereferator.spec_to_extractor(workbook, CellLocation('SHEET1', 'A5'))
    assert dereferator.deref_text('==A1==') == 1
    assert dereferator.deref_text('==A2== world') == 'hello world'
    assert dereferator.deref_text('the value is ==A1==') == 'the value is 1'


def test_deref_pre_spec(workbook):
    dereferator = Dereferator.template_to_spec(workbook, CellLocation('SHEET1', 'A5'))
    assert dereferator.deref_text('<<A1>>') == 1
    assert dereferator.deref_text('<<A2>> world') == 'hello world'
    assert dereferator.deref_text('the value is <<A1>>') == 'the value is 1'
