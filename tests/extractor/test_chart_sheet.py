import openpyxl
import pytest
from os.path import join, dirname

from exco import util


@pytest.fixture
def template():
    fname = join(dirname(__file__),
                 '../../sample/test/chart_sheet_test.xlsx')
    return openpyxl.load_workbook(fname)


def test_iterate_over_chart_sheet(template):
    workbook_cells = util.iterate_cells_in_workbook(workbook=template)
    for cell in workbook_cells:
        assert cell.workbook != 'Chart1'
