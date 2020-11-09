from dataclasses import dataclass
from typing import Any

from exco.extractor.parser.built_in.value_parser import ValueParser


@dataclass
class StringParser(ValueParser[str]):

    def parse_value(self, v: Any) -> str:
        return str(v)
