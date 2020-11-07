import excel_comment_orm as eco
import pytest


@pytest.fixture
def cell_location() -> eco.CellLocation:
    return eco.CellLocation(
        sheet_name='SHEET1',
        coordinate="C29"
    )


def test_short_name(cell_location: eco.CellLocation):
    assert cell_location.short_name == 'SHEET1!C29'


def test_row(cell_location: eco.CellLocation):
    assert cell_location.row == 29


def test_col(cell_location: eco.CellLocation):
    assert cell_location.col == 3


def test_cell_location_has_hash(cell_location: eco.CellLocation):
    assert hash(cell_location) is not None
