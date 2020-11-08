from dataclasses import dataclass
from typing import Any

from excel_comment_orm.cell_full_path import CellFullPath
from excel_comment_orm.exception import ParsingFailException
from excel_comment_orm.extractor.parser.built_in.value_parser import ValueParser
from excel_comment_orm.extractor.parser.parser import Parser
from excel_comment_orm.extractor.parser.pasrsing_result import ParsingResult


@dataclass
class StringParser(ValueParser[str]):

    def parse_value(self, v: Any) -> str:
        try:
            return str(v)
        except ValueError as e:
            raise ParsingFailException(f'Unable to parse {v} to string') from e
