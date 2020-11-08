import abc
from typing import Generic, TypeVar

from excel_comment_orm.cell_full_path import CellFullPath
from excel_comment_orm.extractor.actor import Actor

from excel_comment_orm.extractor.parser.pasrsing_result import ParsingResult

PARSERCLASS_SUFFIX = 'Parser'
T = TypeVar('T')


class Parser(Actor, abc.ABC, Generic[T]):
    @abc.abstractmethod
    def parse(self, cfp: CellFullPath) -> ParsingResult[T]:
        raise NotImplementedError()
