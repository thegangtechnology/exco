from os.path import dirname, join

import pytest

from exco import CellLocation, ExcoTemplate, CellExtractionSpec, LocatorSpec, ExcelProcessorSpec
from exco.exception import ExtractionTaskCreationException, TableExtractionTaskCreationException
from exco.extractor.excel_processor import ProcessorKey, ExcelProcessingResult, ExcelProcessorFactory
from exco.extractor_spec.apv_spec import APVSpec
from exco.extractor_spec.parser_spec import ParserSpec
from exco.extractor_spec.spec_source import UnknownSource
from exco.extractor_spec.table_extraction_spec import TableExtractionSpec, TableItemDirection


@pytest.fixture
def simple_path() -> str:
    return join(dirname(__file__), '../../sample/test/simple.xlsx')


def test_processor_key_hash():
    pk = ProcessorKey(cell_location=CellLocation(
        sheet_name="Sheet",
        coordinate="A1"
    ), key="something")

    assert pk.__hash__() is not None


def test_empty_excel_processing_result():
    epr = ExcelProcessingResult(cell_results={}, table_results={})
    assert epr.cell_result_for_key('a') is None


def test_excel_processor(simple_path: str):
    processor = ExcelProcessorFactory.default().create_from_template_excel(simple_path)
    assert processor.__str__() is not None


def test_fail_extraction_creation(simple_path: str):
    template = ExcoTemplate.from_excel(simple_path)
    spec = template.to_raw_excel_processor_spec()
    spec.cell_specs[CellLocation(sheet_name='TestSheet', coordinate='Z1')] = [CellExtractionSpec(
        locator=LocatorSpec(name="right_of"),
        apv=APVSpec(
            key="something",
            parser=ParserSpec(name='int'),
            source=UnknownSource(),
            validations={},
            fallback=None
        )
    )]

    with pytest.raises(ExtractionTaskCreationException):
        ExcelProcessorFactory.default().create_from_spec(spec=spec).process_workbook(None)


def test_fail_table_creation():
    cl = CellLocation('S', 'A1')
    bad_spec = ExcelProcessorSpec(
        cell_specs={},
        table_specs={cl: [
            TableExtractionSpec(
                key='table',
                locator=LocatorSpec(name='badname'),
                end_conditions=[],
                columns={},
                item_direction=TableItemDirection.DOWNWARD,
                source=UnknownSource()
            )
        ]}
    )
    with pytest.raises(TableExtractionTaskCreationException):
        ExcelProcessorFactory.default().create_from_spec(spec=bad_spec).process_workbook(None)


def test_derefed_processor_process_excel(simple_path: str):
    processor = ExcelProcessorFactory.default().create_from_template_excel(simple_path)
    assert processor.deref(None).process_excel(simple_path) is not None
