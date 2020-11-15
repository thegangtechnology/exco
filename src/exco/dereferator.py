import re
from dataclasses import dataclass
from datetime import date
from re import Pattern
from typing import ClassVar, Union

from openpyxl import Workbook

from exco import CellLocation
from exco.util import CellValue


@dataclass
class Dereferator:
    deref_re: ClassVar[Pattern[str]] = re.compile(r'<<([A-Z]{1,3}\d+)>>')
    workbook: Workbook
    anchor: CellLocation

    def resolve_match(self, coordinate: str) -> CellValue:
        new_loc = self.anchor.new_one_at(coordinate=coordinate)
        cfp = new_loc.get_cell_full_path(self.workbook)
        return cfp.cell.value

    def deref_text(self, text: str) -> CellValue:
        if text and isinstance(text, str):
            # single match return the whole value
            if len(self.deref_re.findall(text)) == 1 and self.deref_re.sub('', text) == '':
                return self.resolve_match(self.deref_re.search(text))

            return self.deref_re.sub(self.resolve_match, str(text))
        else:
            return text
