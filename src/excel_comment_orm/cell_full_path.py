from dataclasses import dataclass

from openpyxl import Workbook
from openpyxl.cell import Cell
from openpyxl.worksheet.worksheet import Worksheet


@dataclass
class CellFullPath:
    workbook: Workbook
    sheet: Worksheet
    cell: Cell
