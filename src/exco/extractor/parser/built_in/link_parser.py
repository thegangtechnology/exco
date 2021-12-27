from dataclasses import dataclass
from datetime import date
from typing import Any, TypeVar

from exco.cell_full_path import CellFullPath
from exco.exception import ParsingFailException
from exco.extractor.parser.built_in.value_parser import ValueParser
from exco.extractor.parser.parsing_result import ParsingResult

T = TypeVar('T')


@dataclass
class LinkResult:
    display: str
    link: str


@dataclass
class LinkParser(ValueParser[date]):

    def parse_value(self, v: Any) -> LinkResult:
        if v.hyperlink:
            return LinkResult(
                display=v.value,
                link=v.hyperlink.target
            )
        else:
            raise ParsingFailException(
                msg=f"{v.coordinate} is not hyperlink"
            )

    def parse(self, cfp: CellFullPath, fallback: T) -> ParsingResult[T]:
        try:
            return ParsingResult.good(self.parse_value(cfp.cell))
        except ParsingFailException as e:
            return ParsingResult.bad(
                msg=f'Parsing {cfp.cell.coordinate} fail.\n'
                    f'value => "{cfp.cell.value}"\n'
                    f'{e.msg}', fallback=fallback, exception=e)
