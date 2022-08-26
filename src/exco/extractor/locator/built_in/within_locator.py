from dataclasses import dataclass
from typing import Optional, Union, Generator

from openpyxl import Workbook
from openpyxl.cell import Cell
from openpyxl.worksheet.merge import MergedCellRange
from openpyxl.worksheet.worksheet import Worksheet

from exco import CellLocation, util
from exco.extractor.locator.locating_result import LocatingResult
from exco.extractor.locator.locator import Locator

CellRange = Union[MergedCellRange, CellLocation]


@dataclass
class WithinLocator(Locator):
    label: str
    type: str
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
                    found_cell = self._search_for_cell(sheet=sheet, cell=cell)
                    if found_cell is None:
                        return LocatingResult.bad(
                            msg=f"Unable to find cell {self.find} to the {self.type.replace('_', ' ')} {self.label}")
                    return LocatingResult.good(found_cell)
        return LocatingResult.bad(
            msg=f"Unable to find cell with label {self.label}")

    def _search_for_cell(self, sheet: Worksheet, cell: Cell) -> Optional[CellLocation]:
        merged_cell = util.get_merged_cell(sheet=sheet, coordinates=cell.coordinate)
        merged_cell = util.coordinate_to_tuple(cell.coordinate) if merged_cell is None else merged_cell
        found_cell = None
        if self.type == "right_of":
            found_cell = self._right_of_scope(sheet=sheet, cell_range=merged_cell)
        elif self.type == "below_of":
            found_cell = self._below_of_scope(sheet=sheet, cell_range=merged_cell)
        if found_cell is None:
            return None
        return self._get_cell_loc(sheet=sheet, cell=found_cell)

    def _get_cell_loc(self, sheet: Worksheet, cell: Cell) -> CellLocation:
        if self.type == "right_of":
            coord = util.get_rightmost_coordinate(sheet=sheet, cell=cell)
            return CellLocation(
                sheet_name=sheet.title,
                coordinate=util.shift_coord(coord.coordinate, (0, 1))
            )
        elif self.type == "below_of":
            coord = util.get_bottommost_coordinate(sheet=sheet, cell=cell)
            return CellLocation(
                sheet_name=sheet.title,
                coordinate=util.shift_coord(coord.coordinate, (1, 0))
            )

    def _right_of_scope(self, sheet: Worksheet, cell_range: CellRange) -> Optional[Cell]:
        # search only rows of merged cell's or cell's column range
        for row in self._cells_by_row_between(sheet=sheet, cell_range=cell_range):
            for cell in row:
                if cell.value == self.find:
                    return cell
        return None

    def _below_of_scope(self, sheet: Worksheet, cell_range: CellRange) -> Optional[Cell]:
        # search only rows of merged cell's or cell's column range
        for col in self._cells_by_col_between(sheet=sheet, cell_range=cell_range):
            for cell in col:
                if cell.value == self.find:
                    return cell
        return None

    def _cells_by_row_between(self, sheet: Worksheet, cell_range: CellRange) -> Generator[Cell, None, None]:
        if type(cell_range) is MergedCellRange:
            min_col = cell_range.max_col
            min_row = cell_range.min_row
            max_col = sheet.max_column
            max_row = cell_range.max_row
        else:
            min_col = cell_range.col
            min_row = cell_range.row
            max_col = sheet.max_column
            max_row = cell_range.row
        for row in range(min_row, max_row + 1):
            cells = (sheet.cell(row=row, column=column) for column in range(min_col, max_col + 1))
            yield tuple(cells)

    def _cells_by_col_between(self, sheet: Worksheet, cell_range: CellRange) -> Generator[Cell, None, None]:
        if type(cell_range) is MergedCellRange:
            min_col = cell_range.min_col
            min_row = cell_range.max_row
            max_col = cell_range.max_col
            max_row = sheet.max_row
        else:
            min_col = cell_range.col
            min_row = cell_range.row
            max_col = cell_range.col
            max_row = sheet.max_row
        for row in range(min_row + 1, max_row + 1):
            cells = (sheet.cell(row=row, column=column) for column in range(min_col, max_col + 1))
            yield tuple(cells)
