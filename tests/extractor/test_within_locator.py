import pytest
from openpyxl.workbook import Workbook

from exco import CellLocation
from exco.cell_full_path import CellFullPath
from exco.extractor.locator.built_in.within_locator import WithinLocator
from exco.extractor.locator.locating_result import LocatingResult


@pytest.fixture
def wb() -> CellFullPath:
    wb = Workbook()

    ws = wb.active

    ws['D2'] = 'top part, should be able to find'

    ws.merge_cells('C3:E19')
    ws['C3'] = 'test table'

    ws['G6'] = 'same name here'
    ws['H6'] = 1

    ws['F3'] = 'top part'
    ws['G3'] = 2

    ws['F19'] = 'below part'
    ws['G19'] = 456

    ws['F13'] = 'test table'
    ws['G13'] = 16

    ws['F20'] = 'unable to find me'  # is exactly 1 cell between merged cells "test table" and "test table 2"

    ws.merge_cells('C21:E32')
    ws['C21'] = 'test table 2'

    ws['G22'] = 'same name here'
    ws['H22'] = 2

    ws['D36'] = 'below of'
    ws['D37'] = 8

    ws['C33'] = 'left part'
    ws['C34'] = 9

    ws['E33'] = 'right part'
    ws['E34'] = 10

    ws['D33'] = 'test table 2'
    ws['D34'] = 11

    ws.merge_cells('C51:E57')
    ws['C51'] = 'test table 3'

    ws['D60'] = 'below of'
    ws['D61'] = 12

    return wb


# RIGHT OF
def test_within_right_of(wb: Workbook):
    rol = WithinLocator(type='right_of', label='test table', find='same name here')
    result = rol.locate(anchor_cell_location=CellLocation(
        sheet_name="Sheet",
        coordinate="A3"
    ), workbook=wb)
    cell_loc = CellLocation(
        sheet_name="Sheet",
        coordinate="H6"
    )
    assert result == LocatingResult.good(cell_loc)


def test_within_right_of_fail(wb: Workbook):
    rol = WithinLocator(type='right_of', label='test table', find='right of')
    result = rol.locate(anchor_cell_location=CellLocation(
        sheet_name="Sheet",
        coordinate="A10"
    ), workbook=wb)
    assert result == LocatingResult.bad(msg="Unable to find cell right of to the right of test table")


def test_within_right_of_boundary_top_check_fail(wb: Workbook):
    rol = WithinLocator(type='right_of', label='test table 2', find='unable to find me')
    result = rol.locate(anchor_cell_location=CellLocation(
        sheet_name="Sheet",
        coordinate="A5"
    ), workbook=wb)
    assert result == LocatingResult.bad(msg="Unable to find cell unable to find me to the right of test table 2")


def test_within_right_of_boundary_below_check_fail(wb: Workbook):
    rol = WithinLocator(type='right_of', label='test table', find='unable to find me')
    result = rol.locate(anchor_cell_location=CellLocation(
        sheet_name="Sheet",
        coordinate="A4"
    ), workbook=wb)
    assert result == LocatingResult.bad(msg="Unable to find cell unable to find me to the right of test table")


def test_within_same_find_right_of(wb: Workbook):
    rol = WithinLocator(type='right_of', label='test table', find='same name here')
    result = rol.locate(anchor_cell_location=CellLocation(
        sheet_name="Sheet",
        coordinate="A6"
    ), workbook=wb)
    cell_loc = CellLocation(
        sheet_name="Sheet",
        coordinate="H6"
    )
    assert result == LocatingResult.good(cell_loc)

    rol = WithinLocator(type='right_of', label='test table 2', find='same name here')
    result = rol.locate(anchor_cell_location=CellLocation(
        sheet_name="Sheet",
        coordinate="A7"
    ), workbook=wb)
    cell_loc = CellLocation(
        sheet_name="Sheet",
        coordinate="H22"
    )
    assert result == LocatingResult.good(cell_loc)


# below OF
def test_within_below_of(wb: Workbook):
    rol = WithinLocator(type='below_of', label='test table', find='below of')
    result = rol.locate(anchor_cell_location=CellLocation(
        sheet_name="Sheet",
        coordinate="B3"
    ), workbook=wb)
    cell_loc = CellLocation(
        sheet_name="Sheet",
        coordinate="D37"
    )
    assert result == LocatingResult.good(cell_loc)


def test_within_below_of_fail(wb: Workbook):
    rol = WithinLocator(type='below_of', label='test table', find='right of')
    result = rol.locate(anchor_cell_location=CellLocation(
        sheet_name="Sheet",
        coordinate="B10"
    ), workbook=wb)
    assert result == LocatingResult.bad(msg="Unable to find cell right of to the below of test table")


def test_within_below_of_boundary_top_check_fail(wb: Workbook):
    rol = WithinLocator(type='below_of', label='test table 2', find='unable to find me')
    result = rol.locate(anchor_cell_location=CellLocation(
        sheet_name="Sheet",
        coordinate="B5"
    ), workbook=wb)
    assert result == LocatingResult.bad(msg="Unable to find cell unable to find me to the below of test table 2")

    rol = WithinLocator(type='below_of', label='test table', find='top part, should be able to find')
    result = rol.locate(anchor_cell_location=CellLocation(
        sheet_name="Sheet",
        coordinate="B5"
    ), workbook=wb)
    assert result == LocatingResult.bad(
        msg="Unable to find cell top part, should be able to find to the below of test table")


def test_within_below_of_boundary_below_check_fail(wb: Workbook):
    rol = WithinLocator(type='below_of', label='test table', find='unable to find me')
    result = rol.locate(anchor_cell_location=CellLocation(
        sheet_name="Sheet",
        coordinate="B4"
    ), workbook=wb)
    assert result == LocatingResult.bad(msg="Unable to find cell unable to find me to the below of test table")


def test_within_same_find_below_of(wb: Workbook):
    rol = WithinLocator(type='below_of', label='test table', find='below of')
    result = rol.locate(anchor_cell_location=CellLocation(
        sheet_name="Sheet",
        coordinate="B6"
    ), workbook=wb)
    cell_loc = CellLocation(
        sheet_name="Sheet",
        coordinate="D37"
    )
    assert result == LocatingResult.good(cell_loc)

    rol = WithinLocator(type='below_of', label='test table 3', find='below of')
    result = rol.locate(anchor_cell_location=CellLocation(
        sheet_name="Sheet",
        coordinate="B7"
    ), workbook=wb)
    cell_loc = CellLocation(
        sheet_name="Sheet",
        coordinate="D61"
    )
    assert result == LocatingResult.good(cell_loc)
