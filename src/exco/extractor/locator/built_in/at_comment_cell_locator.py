from dataclasses import dataclass
from typing import Type, Dict, Any

from exco import CellLocation
from exco.cell_full_path import CellFullPath
from exco.extractor.locator.locating_result import LocatingResult
from exco.extractor.locator.locator import Locator
from openpyxl import Workbook

@dataclass
class AtCommentCellLocator(Locator):

    def locate(self, anchor_cell_location: CellLocation, workbook: Workbook) -> LocatingResult:
        return LocatingResult.good(anchor_cell_location)
