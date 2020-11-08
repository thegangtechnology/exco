import abc
from typing import Any, TypeVar, Type, Dict

from excel_comment_orm.cell_full_path import CellFullPath
from excel_comment_orm.exception import ParsingFailException
from excel_comment_orm.extractor.parser.parser import Parser
from excel_comment_orm.extractor.parser.pasrsing_result import ParsingResult

T = TypeVar('T')


class ValueParser(Parser[T], abc.ABC):

    @abc.abstractmethod
    def parse_value(self, v: Any) -> T:
        raise NotImplementedError()

    def parse(self, cfp: CellFullPath) -> ParsingResult[T]:
        try:
            return ParsingResult.good(self.parse_value(cfp.cell.value))
        except ParsingFailException as e:
            return ParsingResult.bad(f'Parsing {cfp.cell.coordinate} fail.\n'
                                     f'value => "{cfp.cell.value}"\n'
                                     f'{e.msg}',
                                     exception=e)
