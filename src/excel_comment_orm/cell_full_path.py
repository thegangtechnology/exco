from dataclasses import dataclass

from openpyxl import Workbook
from openpyxl.cell import Cell
from openpyxl.worksheet.worksheet import Worksheet


@dataclass
class CellFullPath:
    workbook: Workbook
    sheet: Worksheet
    cell: Cell

    def shift(self, row: int = 0, col: int = 0) -> 'CellFullPath':
        r, c = self.cell.row, self.cell.column
        cell = self.sheet.cell(row=r + row, column=c + col)
        return CellFullPath(
            workbook=self.workbook,
            sheet=self.sheet,
            cell=cell
        )
