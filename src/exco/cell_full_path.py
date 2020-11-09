from dataclasses import dataclass

from openpyxl import Workbook
from openpyxl.cell import Cell
from openpyxl.cell.read_only import EmptyCell
from openpyxl.worksheet.worksheet import Worksheet


@dataclass
class CellFullPath:
    workbook: Workbook
    sheet: Worksheet
    cell: Cell

    def is_blank(self):
        return isinstance(self.cell, EmptyCell) or self.cell.value is None

    def shift(self, row: int = 0, col: int = 0) -> 'CellFullPath':
        r, c = self.cell.row, self.cell.column
        cell = self.sheet.cell(row=r + row, column=c + col)
        return CellFullPath(
            workbook=self.workbook,
            sheet=self.sheet,
            cell=cell
        )
