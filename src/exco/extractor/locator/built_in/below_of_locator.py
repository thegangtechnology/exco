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
    n: int = 1

    def locate(self, anchor_cell_location: CellLocation,
               workbook: Workbook) -> LocatingResult:
        sheet: Worksheet = workbook[anchor_cell_location.sheet_name]
        for row in sheet.iter_rows():
            for cell in row:
                if cell.value == self.label:
                    coord = util.get_bottommost_coordinate(sheet=sheet, cell=cell)
                    cell_loc = CellLocation(
                        sheet_name=anchor_cell_location.sheet_name,
                        coordinate=util.shift_coord(coord.coordinate, (self.n, 0))
                    )
                    return LocatingResult.good(cell_loc)
        return LocatingResult.bad(
            msg=f"Unable to find cell below of {self.label}")
