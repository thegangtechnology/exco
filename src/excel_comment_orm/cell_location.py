from dataclasses import dataclass

from excel_comment_orm.excel_extraction_scope import ExcelExtractionScope
from openpyxl import Workbook
from openpyxl.utils import coordinate_to_tuple
from excel_comment_orm.cell_full_path import CellFullPath
from openpyxl.worksheet.worksheet import Worksheet


@dataclass(frozen=True)
class CellLocation(ExcelExtractionScope):
    sheet_name: str
    coordinate: str

    def __hash__(self):
        return hash((self.sheet_name, self.coordinate))

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
        r, _ = coordinate_to_tuple(self.coordinate)
        return r

    @property
    def col(self) -> int:
        """

        Returns:
            column number
        """
        _, c = coordinate_to_tuple(self.coordinate)
        return c

    def get_cell_full_path(self, wb: Workbook) -> CellFullPath:
        """ Obtain scope object

        Args:
            wb (Workbook):

        Returns:
            CellFullPath
        """
        sheet: Worksheet = wb[self.sheet_name]
        return CellFullPath(
            workbook=wb,
            sheet=sheet,
            cell=sheet[self.coordinate]
        )
