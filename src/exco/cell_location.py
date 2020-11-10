from dataclasses import dataclass
from typing import Tuple

from exco.excel_extraction_scope import ExcelExtractionScope
from exco.util import tuple_to_coordinate
from openpyxl import Workbook
from openpyxl.utils import coordinate_to_tuple
from exco.cell_full_path import CellFullPath
from openpyxl.worksheet.worksheet import Worksheet


@dataclass(frozen=True)
class CellLocation(ExcelExtractionScope):
    """Workbook agnostic cell location."""
    sheet_name: str
    coordinate: str

    def __hash__(self):
        return hash((self.sheet_name, self.coordinate))

    def shift_row(self, offset: int) -> 'CellLocation':
        """Shift the cell by given offset in row direction

        Args:
            offset (int):

        Returns:
            CellLocation
        """
        row, col = self.row_col
        return CellLocation(sheet_name=self.sheet_name, coordinate=tuple_to_coordinate(row + offset, col))

    def shift_col(self, offset: int) -> 'CellLocation':
        """Shift the cell by given offset in column direction.

        Args:
            offset (int):

        Returns:
            CellLocation
        """
        row, col = self.row_col
        return CellLocation(sheet_name=self.sheet_name, coordinate=tuple_to_coordinate(row, col + offset))

    @property
    def short_name(self) -> str:
        """

        Returns:
            short name. Ex: SHEET1!B9
        """
        return f"{self.sheet_name}!{self.coordinate}"

    @property
    def row(self) -> int:
        """

        Returns:
            row number.
        """
        r, _ = self.row_col
        return r

    @property
    def col(self) -> int:
        """

        Returns:
            column number
        """
        _, c = self.row_col
        return c

    @property
    def row_col(self) -> Tuple[int, int]:
        """

        Returns:
            Tuple[int, int]. row, col
        """
        return coordinate_to_tuple(self.coordinate)

    def get_cell_full_path(self, wb: Workbook) -> CellFullPath:
        """ Obtain cell full path

        Args:
            wb (Workbook):

        Returns:
            CellFullPath
        """
        sheet: Worksheet = wb[self.sheet_name]
        return CellFullPath(
            workbook=wb,
            sheetname=self.sheet_name,
            sheet=sheet,
            cell=sheet[self.coordinate]
        )

    def offset_to(self, other: 'CellLocation') -> Tuple[int, int]:
        """Compute offset to another cell
            The offset returned is such that  # our + offset = other
        Args:
            other (CellLocation):

        Returns:
            Tuple[int, int]. row, col
        """
        our_r, our_c = self.row_col
        other_r, other_c = other.row_col
        return other_r - our_r, other_c - our_c
