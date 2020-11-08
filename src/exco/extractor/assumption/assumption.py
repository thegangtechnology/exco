import abc
from typing import Type, TypeVar

from exco.cell_full_path import CellFullPath
from exco.extractor.assumption.assumption_result import AssumptionResult
from exco.extractor.actor import Actor

T = TypeVar('T')


class Assumption(Actor, abc.ABC):
    @abc.abstractmethod
    def assume(self, cfp: CellFullPath) -> AssumptionResult:
        raise NotImplementedError()
