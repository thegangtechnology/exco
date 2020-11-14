import re

from openpyxl import Workbook

from exco import CellLocation
from exco.extractor.locator.built_in.at_comment_cell_locator import AtCommentCellLocator
from exco.extractor.parser.built_in.string_parser import StringParser

DEREF_STYLE = r'<<([A-Z]{1,3}\d+)>>'


def deref_text(workbook: Workbook, sheet_name: str, text: str) -> str:
    """Deref cell values in text
    Returns: str
    """
    def resolve_cell_value(match_obj: re.Match):
        locating_result = AtCommentCellLocator().locate(
            anchor_cell_location=CellLocation(
                sheet_name=sheet_name,
                coordinate=match_obj.group(1)
            ),
            workbook=workbook
        )

        if not locating_result.is_ok:
            raise KeyError()

        cfp = locating_result.location.get_cell_full_path(workbook)
        parsing_result = StringParser().parse(cfp, '')
        return parsing_result.value

    return re.sub(DEREF_STYLE, resolve_cell_value, text)
