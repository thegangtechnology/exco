import abc
from typing import TypeVar

from openpyxl import Workbook

from exco.extractor.actor import Actor

T = TypeVar('T')


class Deref(Actor, abc.ABC):
    @abc.abstractmethod
    def run_deref(self, cell_extraction_task,
                  workbook: Workbook,
                  sheet_name: str) -> str:
        raise NotImplementedError()
