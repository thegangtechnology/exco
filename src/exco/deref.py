import re
from typing import TypeVar

from openpyxl import Workbook

from exco import CellLocation
from exco.extractor.parser.built_in.string_parser import StringParser
from exco.extractor.parser.parser import Parser
from exco.extractor.locator.built_in.at_comment_cell_locator import AtCommentCellLocator

T = TypeVar('T')


class DerefCell:
    def __init__(self, workbook: Workbook, sheet_name: str):
        self.deref_re = re.compile(r'<<([A-Z]{1,3}\d+)>>')
        self.workbook = workbook
        self.sheet_name = sheet_name
        self.parser = None

    def resolve_cell_value(self, cell_coordinate: str):
        locating_result = AtCommentCellLocator().locate(
            anchor_cell_location=CellLocation(
                sheet_name=self.sheet_name,
                coordinate=cell_coordinate
            ),
            workbook=self.workbook
        )

        cfp = locating_result.location.get_cell_full_path(self.workbook)
        parsing_result = self.parser.parse(cfp, '')
        return parsing_result.value

    def resolve_match(self, match_obj: re.Match):
        try:
            return self.resolve_cell_value(match_obj.group(1))
        except ValueError:
            return match_obj.group(0)

    def deref_text(self, text: str, parser: Parser[T] = StringParser()) -> str:
        self.parser = parser
        if text and isinstance(text, str):
            if len(self.deref_re.findall(text)) == 1 and self.deref_re.sub('', text) == '':
                return self.resolve_match(self.deref_re.search(text))

            self.parser = StringParser()
            return self.deref_re.sub(self.resolve_match, str(text))

        return text
