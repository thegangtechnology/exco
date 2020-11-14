from openpyxl import Workbook
from openpyxl.cell import Cell

from exco.cell_full_path import CellFullPath


def test_cell_shift():
    wb = Workbook()

    cell = Cell(row=1, column=2, worksheet=wb)
    cell_full_path = CellFullPath(
        workbook=wb, sheet=wb.active, cell=cell)
    cell_full_path = cell_full_path.shift(3, 5)
    assert cell_full_path.cell.row == 4
    assert cell_full_path.cell.column == 7
