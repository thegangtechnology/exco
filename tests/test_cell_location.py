import exco
import pytest
from exco.cell_location import CellOffset


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
    assert cell_location is not None
    hash(cell_location)


def test_cell_location_offset_to():
    c1 = exco.CellLocation('SHEET1', 'A1')
    c2 = exco.CellLocation('SHEET1', 'C9')
    offset = c1.offset_to(c2)
    assert offset == CellOffset(8, 2)

    c3 = c1.shift(offset)
    assert c3 == c2
