from typing import Dict, Type, Optional

from exco.extractor.base_factory import BaseFactory
from exco.extractor.parser.built_in.date_parser import DateParser
from exco.extractor.parser.built_in.float_parser import FloatParser
from exco.extractor.parser.built_in.int_parser import IntParser
from exco.extractor.parser.built_in.link_parser import LinkParser
from exco.extractor.parser.built_in.string_parser import StringParser
from exco.extractor.parser.parser import Parser
from exco.extractor_spec.parser_spec import ParserSpec


class ParserFactory(BaseFactory[Parser, ParserSpec]):
    def __init__(self, class_map: Dict[str, Type[Parser]]):
        super().__init__(class_map)

    @classmethod
    def suffix(cls):
        return 'Parser'

    @classmethod
    def default(cls, extras: Optional[Dict[str, Type[Parser]]] = None) -> 'ParserFactory':
        defaults = cls.build_class_dict([
            IntParser,
            StringParser,
            FloatParser,
            DateParser,
            LinkParser
        ])
        extras = {} if extras is None else extras
        return cls({**defaults, **extras})
