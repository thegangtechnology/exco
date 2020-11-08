from typing import Dict, Type

from excel_comment_orm.extraction_spec.parser_spec import ParserSpec
from excel_comment_orm.extractor.base_factory import BaseFactory
from excel_comment_orm.extractor.parser.parser import Parser
from excel_comment_orm.extractor.parser.built_in.string_parser import StringParser
from excel_comment_orm.extractor.parser.built_in.int_parser import IntParser
from excel_comment_orm.extractor.parser.built_in.float_parser import FloatParser


class ParserFactory(BaseFactory[Parser, ParserSpec]):
    def __init__(self, class_map: Dict[str, Type[Parser]]):
        super().__init__(class_map)

    @classmethod
    def suffix(self):
        return 'Parser'

    @classmethod
    def default(cls) -> 'ParserFactory':
        return cls(cls.build_class_dict([
            IntParser,
            StringParser,
            FloatParser
        ]))
