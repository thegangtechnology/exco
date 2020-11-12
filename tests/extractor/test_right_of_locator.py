import pytest
from openpyxl import Workbook

from exco import CellLocation
from exco.cell_full_path import CellFullPath
from exco.extractor.locator.built_in.right_of_locator import RightOfLocator
from exco.extractor.locator.built_in.right_of_regex_locator import RightOfRegexLocator
from exco.extractor.locator.locating_result import LocatingResult


@pytest.fixture
def wb() -> CellFullPath:
    wb = Workbook()

    ws = wb.active
    ws['B3'] = 40
    ws['A3'] = 'right of'

    ws['C4'] = 50
    ws['B4'] = 'the key 1'
    return wb


def test_right_of_locator_fail(wb: Workbook):
    rol = RightOfLocator(label='the key')
    result = rol.locate(anchor_cell_location=CellLocation(
        sheet_name="Sheet",
        coordinate="A3"
    ), workbook=wb)
    assert result == LocatingResult.bad(
        msg='Unable to find cell to the right of the key')


def test_right_of_locator_regex(wb: Workbook):
    rol = RightOfRegexLocator(regex='the key\\s\\d')
    result = rol.locate(anchor_cell_location=CellLocation(
        sheet_name="Sheet",
        coordinate="A1"
    ), workbook=wb)
    cell_loc = CellLocation(
        sheet_name="Sheet",
        coordinate="C4"
    )
    assert result == LocatingResult.good(cell_loc)


def test_right_of_locator_regex_failed(wb: Workbook):
    rol = RightOfRegexLocator(regex='the key\\s\\ds')
    result = rol.locate(anchor_cell_location=CellLocation(
        sheet_name="Sheet",
        coordinate="A1"
    ), workbook=wb)
    assert result == LocatingResult.bad(
        msg='Unable to find cell to the right of the key\\s\\ds')
