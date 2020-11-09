from typing import Dict, Type

from exco.extractor_spec.parser_spec import ParserSpec
from exco.extractor.base_factory import BaseFactory
from exco.extractor.parser.built_in.date_parser import DateParser
from exco.extractor.parser.parser import Parser
from exco.extractor.parser.built_in.string_parser import StringParser
from exco.extractor.parser.built_in.int_parser import IntParser
from exco.extractor.parser.built_in.float_parser import FloatParser


class ParserFactory(BaseFactory[Parser, ParserSpec]):
    def __init__(self, class_map: Dict[str, Type[Parser]]):
        super().__init__(class_map)

    @classmethod
    def suffix(cls):
        return 'Parser'

    @classmethod
    def default(cls) -> 'ParserFactory':
        return cls(cls.build_class_dict([
            IntParser,
            StringParser,
            FloatParser,
            DateParser
        ]))
