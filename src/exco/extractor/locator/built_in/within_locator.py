from dataclasses import dataclass
from typing import Optional

from openpyxl import Workbook
from openpyxl.cell import Cell
from openpyxl.worksheet.worksheet import Worksheet

from exco import CellLocation, util
from exco.extractor.locator.locating_result import LocatingResult
from exco.extractor.locator.locator import Locator


@dataclass
class WithinLocator(Locator):
    type: str
    label: str
    find: str

    valid_types = ["right_of", "below_of"]

    def locate(self, anchor_cell_location: CellLocation,
               workbook: Workbook) -> LocatingResult:
        sheet: Worksheet = workbook[anchor_cell_location.sheet_name]
        if self.type not in self.valid_types:
            return LocatingResult.bad(  # might be a better error to throw here
                msg=f"Incorrect type, must be one of the following {self.valid_types}")
        for row in sheet.iter_rows():
            for cell in row:
                if cell.value == self.label:
                    return self._search_for_cell(sheet=sheet, cell=cell)
        return LocatingResult.bad(
            msg=f"Unable to find cell with label {self.label}")

    def _search_for_cell(self, sheet: Worksheet, cell: Cell) -> LocatingResult:
        if self.type == "right_of":
            found_cell = self._right_of_scope(sheet=sheet, cell=cell)
            if found_cell is not None:
                coord = util.get_rightmost_coordinate(sheet=sheet, cell=found_cell)
                cell_loc = CellLocation(
                    sheet_name=sheet.title,
                    coordinate=util.shift_coord(coord.coordinate, (0, 1))
                )
                return LocatingResult.good(cell_loc)
        elif self.type == "below_of":
            found_cell = self._below_of_scope(sheet=sheet, cell=cell)
            if found_cell is not None:
                coord = util.get_bottommost_coordinate(sheet=sheet, cell=found_cell)
                cell_loc = CellLocation(
                    sheet_name=sheet.title,
                    coordinate=util.shift_coord(coord.coordinate, (1, 0))
                )
                return LocatingResult.good(cell_loc)
        return LocatingResult.bad(
            msg=f"Unable to find cell {self.find} to the {self.type.replace('_', ' ')} {self.label}")

    def _right_of_scope(self, sheet: Worksheet, cell: Cell) -> Optional[Cell]:
        for row in util.iter_rows_between(sheet=sheet, cell=cell):
            for cell in row:
                if cell.value == self.find:
                    return cell
        return None

    def _below_of_scope(self, sheet: Worksheet, cell: Cell) -> Optional[Cell]:
        for col in util.iter_cols_between(sheet=sheet, cell=cell):
            for cell in col:
                if cell.value == self.find:
                    return cell
        return None
