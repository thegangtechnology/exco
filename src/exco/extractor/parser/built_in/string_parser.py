from dataclasses import dataclass
from typing import Any

from exco.cell_full_path import CellFullPath
from exco.exception import ParsingFailException
from exco.extractor.parser.built_in.value_parser import ValueParser
from exco.extractor.parser.parser import Parser
from exco.extractor.parser.pasrsing_result import ParsingResult


@dataclass
class StringParser(ValueParser[str]):

    def parse_value(self, v: Any) -> str:
        try:
            return str(v)
        except ValueError as e:
            raise ParsingFailException(f'Unable to parse {v} to string') from e
