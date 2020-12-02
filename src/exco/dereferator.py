import re
from dataclasses import dataclass
from typing import Pattern

from exco import CellLocation, setting
from exco.util import CellValue
from openpyxl import Workbook


@dataclass
class Dereferator:
    deref_re: Pattern
    workbook: Workbook
    anchor: CellLocation

    def resolve_coordinate(self, coordinate: str) -> CellValue:
        """Resolve string coordinate ex: A1 to cell value

        Args:
            coordinate (str): cell's coordinate

        Returns:
            CellValue
        """
        new_loc = self.anchor.new_one_at(coordinate=coordinate)
        cfp = new_loc.get_cell_full_path(self.workbook)
        return cfp.cell.value

    def resolve_match(self, match_obj: re.Match) -> CellValue:
        """Resolve value from regex MatchObject

        Args:
            match_obj (re.Match):

        Returns:
            CellValue
        """
        return self.resolve_coordinate(match_obj.group(1))

    def deref_text(self, text: str) -> CellValue:
        """Deref Text.
        If the type is string and it contains fully the pattern (pure match), then the return type
        is exactly the cell.value. Ex: '<<A1>>' -> 1
        If string contains any other string then the return value is a string substitution.
        Ex: 'the value is <<A1>>' -> 'the value is 1
        Args:
            text (str): text

        Returns:
            CellValue
        """
        if text and isinstance(text, str):
            # single match return the whole value
            pure_match = len(self.deref_re.findall(text)) == 1 and self.deref_re.sub('', text) == ''
            if pure_match:
                return self.resolve_match(self.deref_re.search(text))
            else:  # otherwise do simple string interpolation
                def str_resolve(x):
                    return str(self.resolve_match(x))

                return self.deref_re.sub(str_resolve, str(text))
        else:
            return text

    @classmethod
    def template_to_spec(cls, workbook: Workbook, anchor: CellLocation):
        return Dereferator(
            deref_re=setting.template_to_spec_deref_re,
            workbook=workbook,
            anchor=anchor
        )

    @classmethod
    def spec_to_extractor(cls, workbook: Workbook, anchor: CellLocation):
        return Dereferator(
            deref_re=setting.spec_to_extractor_deref_re,
            workbook=workbook,
            anchor=anchor
        )
