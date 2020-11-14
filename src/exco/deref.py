import re
from typing import TypeVar

from openpyxl import Workbook

from exco import CellLocation
from exco.extractor.parser.built_in.string_parser import StringParser
from exco.extractor.parser.parser import Parser
from exco.extractor.locator.built_in.at_comment_cell_locator import AtCommentCellLocator

DEREF_STYLE = r'<<([A-Z]{1,3}\d+)>>'

T = TypeVar('T')


def deref_text(workbook: Workbook, sheet_name: str, parser: Parser[T], text: str) -> str:
    """Deref cell values in text
    Returns: str
    """

    def resolve_cell_value(cell_coordinate: str):
        locating_result = AtCommentCellLocator().locate(
            anchor_cell_location=CellLocation(
                sheet_name=sheet_name,
                coordinate=cell_coordinate
            ),
            workbook=workbook
        )

        cfp = locating_result.location.get_cell_full_path(workbook)
        parsing_result = parser.parse(cfp, '')
        return parsing_result.value

    def resolve_match(match_obj: re.Match):
        try:
            return resolve_cell_value(match_obj.group(1))
        except ValueError:
            return match_obj.group(0)

    deref_re = re.compile(DEREF_STYLE)
    if text and isinstance(text, str):
        if len(deref_re.findall(text)) == 1 and deref_re.sub('', text) == '':
            return resolve_match(deref_re.search(text))

        parser = StringParser()
        return re.sub(DEREF_STYLE, resolve_match, str(text))

    return text
