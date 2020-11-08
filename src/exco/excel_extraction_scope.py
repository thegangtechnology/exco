import abc
from typing import TypeVar

from exco.cell_full_path import CellFullPath
from openpyxl import Workbook

T = TypeVar('T')


class ExcelExtractionScope(abc.ABC):

    @abc.abstractmethod
    def get_cell_full_path(self, wb: Workbook) -> CellFullPath:
        raise NotImplementedError()
