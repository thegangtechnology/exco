from dataclasses import dataclass

from openpyxl import Workbook

from exco.extractor.deref.deref_cell import DerefCell
from exco.extractor.cell_extraction_task import CellExtractionTask
from exco.extractor.deref.deref import Deref


@dataclass
class EverythingDeref(Deref):
    def run_deref(self, cell_extraction_task: CellExtractionTask,
                  workbook: Workbook,
                  sheet_name: str) -> CellExtractionTask:
        dc = DerefCell(workbook=workbook,
                       sheet_name=sheet_name)

        cell_extraction_task.key = dc.deref_text(cell_extraction_task.key)
        cell_extraction_task.fallback = dc.deref_text(cell_extraction_task.fallback,
                                                      parser=cell_extraction_task.parser)

        if hasattr(cell_extraction_task.locator, 'label'):
            cell_extraction_task.locator.label = dc.deref_text(cell_extraction_task.locator.label)
