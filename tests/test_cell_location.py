import exco
import pytest


@pytest.fixture
def cell_location() -> exco.CellLocation:
    return exco.CellLocation(
        sheet_name='SHEET1',
        coordinate="C29"
    )


def test_short_name(cell_location: exco.CellLocation):
    assert cell_location.short_name == 'SHEET1!C29'


def test_row(cell_location: exco.CellLocation):
    assert cell_location.row == 29


def test_col(cell_location: exco.CellLocation):
    assert cell_location.col == 3


def test_cell_location_has_hash(cell_location: exco.CellLocation):
    assert hash(cell_location) is not None
