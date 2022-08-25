from dataclasses import dataclass

from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet

from exco import CellLocation, util
from exco.extractor.locator.locating_result import LocatingResult
from exco.extractor.locator.locator import Locator


@dataclass
class SearchRightOfLocator(Locator):
    label: str
    max_empty_col_search: int

    def locate(self, anchor_cell_location: CellLocation,
               workbook: Workbook) -> LocatingResult:
        sheet: Worksheet = workbook[anchor_cell_location.sheet_name]
        for row in sheet.iter_rows():
            for cell in row:
                if cell.value == self.label:
                    coord = util.get_rightmost_coordinate(sheet=sheet, cell=cell)
                    cell_cor = self._search_empty_col(coord.coordinate, sheet)
                    cell_loc = CellLocation(
                        sheet_name=anchor_cell_location.sheet_name,
                        coordinate=cell_cor
                    )
                    return LocatingResult.good(cell_loc)
        return LocatingResult.bad(
            msg=f"Unable to find cell to the right of {self.label}")

    def _search_empty_col(self, cell_cor: str, sheet: Worksheet) -> str:
        for i in range(0, self.max_empty_col_search):
            cell_cor = util.shift_coord(cell_cor, (0, 1))
            if sheet[cell_cor].value is not None:
                return cell_cor
        return cell_cor
