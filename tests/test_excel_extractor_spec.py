from os.path import join, dirname

import pytest
from excel_comment_orm import ExcelTemplate
from excel_comment_orm.extraction_spec.excel_extrator_spec import ExcelExtractorSpec


@pytest.fixture
def simple_spec():
    template = ExcelTemplate.from_excel(join(dirname(__file__), '../sample/test/simple.xlsx'))
    spec = template.to_excel_extractor_spec()
    return spec


def test_spec(simple_spec: ExcelExtractorSpec):
    assert simple_spec.n_spec() == 3
    assert simple_spec.n_location() == 2
