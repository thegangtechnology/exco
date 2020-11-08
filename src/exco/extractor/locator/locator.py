import abc
from typing import Dict, Any, Type, TypeVar

from exco.cell_full_path import CellFullPath
from exco.cell_location import CellLocation
from exco.extractor.actor import Actor
from exco.extractor.locator.locating_result import LocatingResult
from openpyxl import Workbook

T = TypeVar('T')


class Locator(Actor, abc.ABC):
    @abc.abstractmethod
    def locate(self, anchor_cell_location: CellLocation, workbook: Workbook) -> LocatingResult:
        raise NotImplementedError()
