from os.path import join, dirname

import pytest
from excel_comment_orm import ECOTemplate
from excel_comment_orm.extraction_spec.excel_processor_spec import ExcelProcessorSpec


@pytest.fixture
def simple_spec():
    template = ECOTemplate.from_excel(join(dirname(__file__), '../sample/test/simple.xlsx'))
    spec = template.to_excel_extractor_spec()
    return spec


def test_spec(simple_spec: ExcelProcessorSpec):
    assert simple_spec.n_spec() == 3
    assert simple_spec.n_location() == 2
