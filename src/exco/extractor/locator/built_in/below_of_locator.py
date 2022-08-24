from dataclasses import dataclass

from openpyxl import Workbook

from exco import CellLocation, util
from exco.extractor.locator.locating_result import LocatingResult
from exco.extractor.locator.locator import Locator
from openpyxl.worksheet.worksheet import Worksheet


@dataclass
class BelowOfLocator(Locator):
    """Resolve to the cell below the anchored cell"""
    label: str
    max_empty_row_search: int = 0

    def locate(self, anchor_cell_location: CellLocation,
               workbook: Workbook) -> LocatingResult:
        sheet: Worksheet = workbook[anchor_cell_location.sheet_name]
        for row in sheet.iter_rows():
            for cell in row:
                if cell.value == self.label:
                    cell_cor = util.shift_coord(cell.coordinate, (1, 0))
                    if self.max_empty_row_search != 0:
                        return self._empty_row_search(cell_cor, sheet, anchor_cell_location)
                    cell_loc = CellLocation(
                        sheet_name=anchor_cell_location.sheet_name,
                        coordinate=cell_cor
                    )
                    return LocatingResult.good(cell_loc)
        return LocatingResult.bad(
            msg=f"Unable to find cell below of {self.label}")

    def _empty_row_search(self, cell_cor: str, sheet: Worksheet,
                          anchor_cell_location: CellLocation) -> LocatingResult:
        for i in range(0, self.max_empty_row_search-1):
            cell_cor = util.shift_coord(cell_cor, (1, 0))
            if sheet[cell_cor].value is not None:
                cell_loc = CellLocation(
                    sheet_name=anchor_cell_location.sheet_name,
                    coordinate=cell_cor
                )
                return LocatingResult.good(cell_loc)
        return LocatingResult.bad(
                    msg=f"Unable to find cell below of {self.label}")
