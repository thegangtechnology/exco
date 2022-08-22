from dataclasses import dataclass

from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet

from exco import CellLocation, util
from exco.extractor.locator.locating_result import LocatingResult
from exco.extractor.locator.locator import Locator


@dataclass
class RightOfLocator(Locator):  # TODO: Add search scope
    label: str
    maximum_column = int

    def locate(self, anchor_cell_location: CellLocation,
               workbook: Workbook) -> LocatingResult:
        sheet: Worksheet = workbook[anchor_cell_location.sheet_name]
        for row in sheet.iter_rows():
            for cell in row:
                if cell.value == self.label:
                    if self._is_merged_cell(sheet, cell.coordinate):
                        coord = (cell.row,
                                 self._get_rightmost_column(sheet, cell.coordinate))
                        cell_loc = CellLocation(
                            sheet_name=anchor_cell_location.sheet_name,
                            coordinate=util.shift_coord(util.tuple_to_coordinate(coord[0], coord[1]),
                                                        (0, 1))
                        )
                    else:
                        cell_loc = CellLocation(
                            sheet_name=anchor_cell_location.sheet_name,
                            coordinate=util.shift_coord(cell.coordinate,(0, 1))
                        )
                    return LocatingResult.good(cell_loc)
        return LocatingResult.bad(
            msg=f"Unable to find cell to the right of {self.label}")

    def _is_merged_cell(self, sheet: Worksheet, coordinates: CellLocation) -> bool:
        for merged_cell in sheet.merged_cell_ranges:
            if coordinates in merged_cell:
                return True
        return False
    def _get_rightmost_column(self, sheet: Worksheet, coordinates: CellLocation) -> maximum_column:
        for merged_cell in sheet.merged_cell_ranges:
            if coordinates in merged_cell:
                return merged_cell.max_col
