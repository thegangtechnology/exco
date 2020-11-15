from dataclasses import dataclass

from openpyxl import Workbook

from exco.extractor.cell_extraction_task import CellExtractionTask
from exco.extractor.deref.deref import Deref


@dataclass
class NoDeref(Deref):
    def run_deref(self, cell_extraction_task: CellExtractionTask,
                  workbook: Workbook,
                  sheet_name: str) -> CellExtractionTask:
        pass  # We don't want to run any deref
