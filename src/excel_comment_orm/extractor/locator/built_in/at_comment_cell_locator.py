from dataclasses import dataclass
from typing import Type, Dict, Any

from excel_comment_orm import CellLocation
from excel_comment_orm.cell_full_path import CellFullPath
from excel_comment_orm.extractor.locator.locating_result import LocatingResult
from excel_comment_orm.extractor.locator.locator import Locator
from openpyxl import Workbook

@dataclass
class AtCommentCellLocator(Locator):

    def locate(self, anchor_cell_location: CellLocation, workbook: Workbook) -> LocatingResult:
        return LocatingResult.good(anchor_cell_location)
