from dataclasses import dataclass

from openpyxl import Workbook

from exco import CellLocation
from exco.extractor.locator.locating_result import LocatingResult
from exco.extractor.locator.locator import Locator


@dataclass
class AtCommentCellLocator(Locator):

    def locate(self, anchor_cell_location: CellLocation, workbook: Workbook) -> LocatingResult:
        return LocatingResult.good(anchor_cell_location)
