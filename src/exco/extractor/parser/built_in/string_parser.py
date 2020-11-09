from dataclasses import dataclass
from typing import Any

from exco.exception import ParsingFailException
from exco.extractor.parser.built_in.value_parser import ValueParser


@dataclass
class StringParser(ValueParser[str]):

    def parse_value(self, v: Any) -> str:
        try:
            return str(v)
        except ValueError as e:
            raise ParsingFailException(f'Unable to parse {v} to string') from e
