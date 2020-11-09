from os.path import dirname, join

import pytest

from exco import CellLocation, ExcoTemplate, ExtractionTaskSpec, LocatorSpec
from exco.extractor.excel_processor import ProcessorKey, ExcelProcessingResult, ExcelProcessorFactory


def test_processor_key_hash():
    pk = ProcessorKey(cell_location=CellLocation(
        sheet_name="Sheet",
        coordinate="A1"
    ), key="something")

    assert pk.__hash__() is not None


def test_empty_excel_processing_result():
    epr = ExcelProcessingResult(results={})
    assert epr.for_key('a') is None


def test_excel_processor():
    fname = join(dirname(__file__), '../../sample/test/simple.xlsx')
    processor = ExcelProcessorFactory.default().create_from_template_excel(fname)
    assert processor.__str__() is not None


def test_fail_extraction_task():
    fname = join(dirname(__file__), '../../sample/test/simple.xlsx')
    template = ExcoTemplate.from_excel(fname)
    spec = template.to_excel_extractor_spec()
    spec.task_specs[CellLocation(sheet_name='TestSheet', coordinate='Z1')] = [ExtractionTaskSpec(
        key="something",
        locator=LocatorSpec(name="right_of"),
        parser=None,
        source=None,
        validations={}
    )]

    with pytest.raises(AttributeError):
        ExcelProcessorFactory.default().create_from_spec(spec=spec)