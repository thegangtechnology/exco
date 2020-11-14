from unittest.mock import patch

import pytest
from openpyxl import Workbook

from exco import CellLocation
from exco.extractor import Locator


@patch.multiple(Locator, __abstractmethods__=set())
def test_location_abstract():
    with pytest.raises(NotImplementedError):
        locator = Locator()
        locator.locate(anchor_cell_location=CellLocation(
            sheet_name="Sheet",
            coordinate="A1"
        ), workbook=Workbook())
