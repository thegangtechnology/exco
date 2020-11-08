from typing import Any

from excel_comment_orm.cell_full_path import CellFullPath
from excel_comment_orm.exception import ParsingFailException
from excel_comment_orm.extractor.parser.built_in.value_parser import ValueParser
from excel_comment_orm.extractor.parser.parser import Parser
from excel_comment_orm.extractor.parser.pasrsing_result import ParsingResult


class FloatParser(ValueParser[float]):

    def parse_value(self, v: Any) -> float:
        try:
            return float(v)
        except ValueError as e:
            raise ParsingFailException(f'Fail parsing {v} to float.') from e
