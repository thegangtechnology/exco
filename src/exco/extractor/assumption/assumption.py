import abc
from typing import TypeVar

from exco.cell_full_path import CellFullPath
from exco.extractor.actor import Actor
from exco.extractor.assumption.assumption_result import AssumptionResult

T = TypeVar('T')


class Assumption(Actor, abc.ABC):
    @abc.abstractmethod
    def assume(self, cfp: CellFullPath) -> AssumptionResult:
        raise NotImplementedError()
