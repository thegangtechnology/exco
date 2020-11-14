from exco import CellLocation
from exco.extractor.locator.built_in.below_locator import BelowLocator

import pytest
from openpyxl import Workbook


@pytest.fixture()
def blank_workbook():
    wb = Workbook()
    return wb


def test_below_locator(blank_workbook):
    loc = BelowLocator()
    cell_loc = CellLocation(sheet_name='SHEET1', coordinate='A1')
    got = loc.locate(cell_loc, blank_workbook)
    assert got.location == CellLocation(sheet_name='SHEET1', coordinate='A2')
