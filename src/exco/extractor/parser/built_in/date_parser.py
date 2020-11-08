from dataclasses import dataclass
from datetime import date, datetime
from typing import Any

from exco.exception import ParsingFailException
from exco.extractor.parser.built_in.value_parser import ValueParser


@dataclass
class DateParser(ValueParser[date]):

    def parse_value(self, v: Any) -> date:
        if isinstance(v, datetime):
            return v.date()
        else:
            raise ParsingFailException(f'{v} is not datetime')
