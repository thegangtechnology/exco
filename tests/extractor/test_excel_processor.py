from os.path import dirname, join

import pytest

from exco import CellLocation, ExcoTemplate, CellExtractionSpec, LocatorSpec
from exco.exception import ExtractionTaskCreationException
from exco.extractor.excel_processor import ProcessorKey, ExcelProcessingResult, ExcelProcessorFactory
from exco.extractor_spec.apv_spec import APVSpec


def test_processor_key_hash():
    pk = ProcessorKey(cell_location=CellLocation(
        sheet_name="Sheet",
        coordinate="A1"
    ), key="something")

    assert pk.__hash__() is not None


def test_empty_excel_processing_result():
    epr = ExcelProcessingResult(cell_results={}, table_results={})
    assert epr.cell_result_for_key('a') is None


def test_excel_processor():
    fname = join(dirname(__file__), '../../sample/test/simple.xlsx')
    processor = ExcelProcessorFactory.default().create_from_template_excel(fname)
    assert processor.__str__() is not None


def test_fail_extraction_task():
    fname = join(dirname(__file__), '../../sample/test/simple.xlsx')
    template = ExcoTemplate.from_excel(fname)
    spec = template.to_excel_extractor_spec()
    spec.cell_specs[CellLocation(sheet_name='TestSheet', coordinate='Z1')] = [CellExtractionSpec(
        locator=LocatorSpec(name="right_of"),
        apv=APVSpec(
            key="something",
            parser=None,
            source=None,
            validations={}
        )
    )]

    with pytest.raises(ExtractionTaskCreationException):
        ExcelProcessorFactory.default().create_from_spec(spec=spec)
