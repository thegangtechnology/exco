import abc
from typing import Type, TypeVar

from excel_comment_orm.cell_full_path import CellFullPath
from excel_comment_orm.extractor.assumption.assumption_result import AssumptionResult
from excel_comment_orm.extractor.actor import Actor

T = TypeVar('T')


class Assumption(Actor, abc.ABC):
    @abc.abstractmethod
    def assume(self, cfp: CellFullPath) -> AssumptionResult:
        raise NotImplementedError()
