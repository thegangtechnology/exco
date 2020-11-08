import abc
import re
from dataclasses import dataclass
from typing import Optional

from excel_comment_orm import util
from excel_comment_orm.cell_location import CellLocation
from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet


class Locator(abc.ABC):
    @abc.abstractmethod
    def locate(self, comment_cell: CellLocation, workbook: Workbook) -> CellLocation:
        pass


class AtCommentCellLocator(Locator):

    def locate(self, comment_cell: CellLocation, workbook: Workbook) -> CellLocation:
        return comment_cell


class RightOfLocator(Locator):  # TODO: Add search scope
    label: str

    def locate(self, comment_cell: CellLocation, workbook: Workbook) -> Optional[CellLocation]:
        sheet: Worksheet = workbook[comment_cell.sheet_name]
        compiled_regex = re.compile(self.regex)
        for row in sheet.iter_rows():
            for cell in row:
                if cell.value == self.label:
                    return CellLocation(
                        sheet_name=comment_cell.sheet_name,
                        coordinate=util.shift_coord(cell.coordinate, (0, 1))
                    )
        return None


@dataclass(frozen=True)
class RightOfRegexLocator(Locator):
    regex: str

    def locate(self, comment_cell: CellLocation, workbook: Workbook) -> Optional[CellLocation]:
        sheet: Worksheet = workbook[comment_cell.sheet_name]
        compiled_regex = re.compile(self.regex)
        for row in sheet.iter_rows():
            for cell in row:
                if compiled_regex.fullmatch(row) is not None:
                    return CellLocation(
                        sheet_name=comment_cell.sheet_name,
                        coordinate=util.shift_coord(cell.coordinate, (0, 1))
                    )
        return None
