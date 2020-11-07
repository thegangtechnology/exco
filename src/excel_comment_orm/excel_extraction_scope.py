import abc
from dataclasses import dataclass
from typing import TypeVar, Generic

from openpyxl import Workbook
from openpyxl.cell import Cell
from openpyxl.worksheet.worksheet import Worksheet

T = TypeVar('T')


@dataclass
class CellFullPath:
    workbook: Workbook
    sheet: Worksheet
    cell: Cell


class ExcelExtractionScope(abc.ABC):

    @abc.abstractmethod
    def get_cell_full_path(self, wb: Workbook) -> CellFullPath:
        raise NotImplementedError()
    
