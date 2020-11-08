from os.path import join, dirname

import pytest
import exco


@pytest.fixture
def simple_spec():
    template = exco.ExcoTemplate.from_excel(join(dirname(__file__), '../../sample/test/simple.xlsx'))
    spec = template.to_excel_extractor_spec()
    return spec


def test_spec(simple_spec: exco.ExcelProcessorSpec):
    assert simple_spec.n_spec() == 3
    assert simple_spec.n_location() == 2
