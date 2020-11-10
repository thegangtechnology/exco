from dataclasses import dataclass
from typing import Any

from exco.exception import ParsingFailException
from exco.extractor.parser.built_in.value_parser import ValueParser


@dataclass
class IntParser(ValueParser[int]):

    def parse_value(self, v: Any) -> int:
        try:
            return int(v)  # fix this it shouldn't parse float
        except Exception as e:
            raise ParsingFailException(f'Unable to parse {v} to int') from e
