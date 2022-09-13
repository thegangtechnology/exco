from dataclasses import dataclass

from openpyxl import Workbook
from openpyxl.cell import Cell
from openpyxl.worksheet.worksheet import Worksheet

from exco import CellLocation, util
from exco.extractor.locator.locating_result import LocatingResult
from exco.extractor.locator.locator import Locator


@dataclass
class WithinLocator(Locator):
    label: str
    find: str
    direction: str
    perform: str
    n: int = 1

    valid_directions = ["right_of", "below_of"]

    def locate(self, anchor_cell_location: CellLocation,
               workbook: Workbook) -> LocatingResult:
        sheet: Worksheet = workbook[anchor_cell_location.sheet_name]
        if self.direction not in self.valid_directions:
            return LocatingResult.bad(
                msg=f"Incorrect direction, must be one of the following {self.valid_directions}")
        if self.perform not in self.valid_directions:  # might be a better errors to throw here
            return LocatingResult.bad(
                msg=f"Incorrect perform, must be one of the following {self.valid_directions}")
        for row in sheet.iter_rows():
            for cell in row:
                if cell.value == self.label:
                    return self._search_for_cell(sheet=sheet, cell=cell)
        return LocatingResult.bad(
            msg=f"Unable to find cell with label {self.label}")

    def _search_for_cell(self, sheet: Worksheet, cell: Cell) -> LocatingResult:
        found_cell = None
        if self.direction == "right_of":
            found_cell = util.search_right_of_scope(sheet=sheet, cell=cell, label=self.find)
        elif self.direction == "below_of":
            found_cell = util.search_below_of_scope(sheet=sheet, cell=cell, label=self.find)
        if found_cell is None:
            return LocatingResult.bad(
                msg=f"Unable to find cell {self.find} to the {self.direction.replace('_', ' ')} {self.label}")
        cell_loc = self._get_cell(sheet=sheet, cell=found_cell)
        return LocatingResult.good(cell_loc)

    def _get_cell(self, sheet: Worksheet, cell: Cell) -> CellLocation:
        if self.perform == "right_of":
            coord = util.get_rightmost_coordinate(sheet=sheet, cell=cell)
            return CellLocation(
                sheet_name=sheet.title,
                coordinate=util.shift_coord(coord.coordinate, (0, self.n))
            )
        if self.perform == "below_of":
            coord = util.get_bottommost_coordinate(sheet=sheet, cell=cell)
            return CellLocation(
                sheet_name=sheet.title,
                coordinate=util.shift_coord(coord.coordinate, (self.n, 0))
            )
