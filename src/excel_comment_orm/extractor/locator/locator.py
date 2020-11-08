import abc
from typing import Dict, Any, Type, TypeVar

from excel_comment_orm.cell_full_path import CellFullPath
from excel_comment_orm.cell_location import CellLocation
from excel_comment_orm.extractor.actor import Actor
from excel_comment_orm.extractor.locator.locating_result import LocatingResult
from openpyxl import Workbook

T = TypeVar('T')


class Locator(Actor, abc.ABC):
    @abc.abstractmethod
    def locate(self, anchor_cell_location: CellLocation, workbook: Workbook) -> LocatingResult:
        raise NotImplementedError()
