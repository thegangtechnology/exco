import abc
from typing import Any, TypeVar

from exco.cell_full_path import CellFullPath
from exco.exception import ParsingFailException
from exco.extractor.parser.parser import Parser
from exco.extractor.parser.parsing_result import ParsingResult

T = TypeVar('T')


class ValueParser(Parser[T], abc.ABC):

    @abc.abstractmethod
    def parse_value(self, v: Any) -> T:
        raise NotImplementedError()

    def parse(self, cfp: CellFullPath, fallback: T) -> ParsingResult[T]:
        try:
            return ParsingResult.good(self.parse_value(cfp.cell.value))
        except ParsingFailException as e:
            return ParsingResult.bad(
                msg=f'Parsing {cfp.cell.coordinate} fail.\n'
                f'value => "{cfp.cell.value}"\n'
                f'{e.msg}', fallback=fallback, exception=e)
