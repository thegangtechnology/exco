import openpyxl
import pytest
from os.path import join, dirname

from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet

import exco
from exco import ExcelProcessorSpec, CellLocation, CellExtractionSpec, util
from exco.extractor_spec.apv_spec import APVSpec
from exco.extractor_spec.parser_spec import ParserSpec


@pytest.fixture
def template():
    fname = join(dirname(__file__),
                 '../../sample/test/chart_sheet_test.xlsx')
    return fname


sheet_checkers = {
    "chart_sheet": lambda name: "chart" in name.lower()
}


def test_iterate_over_chart_sheet(template):
    workbook: Workbook = openpyxl.load_workbook(template)
    workbook_cells = util.iterate_cells_in_workbook(workbook=workbook)
    for cell in workbook_cells:
        assert cell.workbook != 'Chart1'


def test_forced_insert_spec_into_chart_sheet(template):
    workbook: Workbook = openpyxl.load_workbook(template)
    assert set(workbook.sheetnames) == {'Sheet1', 'Chart1', 'Sheet2', 'Sheet3'}
    test_spec = ExcelProcessorSpec(table_specs={},
                                   cell_specs={
                                       CellLocation(sheet_name="Chart1", coordinate="A1"):
                                           [
                                               CellExtractionSpec(
                                                   apv=APVSpec(
                                                       key="chart_key",
                                                       parser=ParserSpec(name="string"),
                                                       fallback=None
                                                   )
                                               )
                                           ]
                                   })
    processor = exco.from_excel(
        fname=template,
        sheet_name_checkers=sheet_checkers
    )
    dereffed_processor = processor.factory.create_derefed_processor_from_spec(test_spec)
    try:
        dereffed_processor.process_workbook(workbook)
        assert False
    except TypeError as e:
        assert str(e) == "'Chartsheet' object is not subscriptable"


def test_chart_sheet_not_found_in_results(template):
    workbook: Workbook = openpyxl.load_workbook(template)
    processor = exco.from_excel(
        fname=template,
        sheet_name_checkers=sheet_checkers
    )
    for cell in processor.spec.cell_specs:
        assert cell.sheet_name != 'Chart1'
    result = processor.process_workbook(workbook)
    assert result.to_dict() == {'key': 10, 'key2': 90, 'key3': 'Hello'}
    for cell_result in result.cell_results:
        assert cell_result.sheet_name != 'Chart1'
