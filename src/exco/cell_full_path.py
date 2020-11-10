from dataclasses import dataclass

from openpyxl import Workbook
from openpyxl.cell import Cell
from openpyxl.cell.read_only import EmptyCell
from openpyxl.worksheet.worksheet import Worksheet


@dataclass
class CellFullPath:
    workbook: Workbook
    sheetname: str  # todo: make sheetname a property from sheet.title
    sheet: Worksheet
    cell: Cell

    def is_blank(self):
        """

        Returns:
            True if cell is blank.
        """
        return isinstance(self.cell, EmptyCell) or self.cell.value is None

    def shift(self, row: int = 0, col: int = 0) -> 'CellFullPath':
        """Shift cell full path by row and column

        Args:
            row (int):
            col (int):

        Returns:
            CellFullPath
        """
        r, c = self.cell.row, self.cell.column
        cell = self.sheet.cell(row=r + row, column=c + col)
        return CellFullPath(
            workbook=self.workbook,
            sheetname=self.sheetname,
            sheet=self.sheet,
            cell=cell
        )

    def to_cell_location(self) -> 'CellLocation':
        """Convert to workbook agnostic cell location.
        Returns:
            CellLocation
        """
        from exco.cell_location import CellLocation
        return CellLocation(sheet_name=self.sheetname, coordinate=self.cell.coordinate)
