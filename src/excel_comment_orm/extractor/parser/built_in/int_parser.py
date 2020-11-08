from dataclasses import dataclass
from typing import Any

from excel_comment_orm.exception import ParsingFailException
from excel_comment_orm.extractor.parser.built_in.value_parser import ValueParser


@dataclass
class IntParser(ValueParser[int]):

    def parse_value(self, v: Any) -> int:
        try:
            return int(v)  # fix this it shouldn't parse float
        except ValueError as e:
            raise ParsingFailException(f'Unable to parse {v} to int') from e
