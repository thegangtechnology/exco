from dataclasses import dataclass
from typing import Any

from exco.exception import ParsingFailException
from exco.extractor.parser.built_in.value_parser import ValueParser


@dataclass
class FloatParser(ValueParser[float]):

    def parse_value(self, v: Any) -> float:
        try:
            return float(v)
        except (TypeError, ValueError) as e:
            raise ParsingFailException(f'Fail parsing {v} to float.') from e
