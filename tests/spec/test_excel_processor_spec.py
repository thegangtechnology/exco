from os.path import join, dirname

import pytest
import exco


@pytest.fixture
def simple_spec():
    template = exco.ExcoTemplate.from_excel(
        join(dirname(__file__), '../../sample/test/simple.xlsx'))
    spec = template.to_raw_excel_processor_spec()
    return spec


def test_from_excel_template():
    template = exco.ExcelProcessorSpec.from_excel_template(
        join(dirname(__file__), '../../sample/test/simple.xlsx'))
    assert template is not None


def test_spec(simple_spec: exco.ExcelProcessorSpec):
    assert simple_spec.n_cell_spec() == 3
    assert simple_spec.n_cell_location() == 2


def test_unique_key(simple_spec: exco.ExcelProcessorSpec):
    assert simple_spec.is_keys_unique()


def test_not_unique_key(simple_spec: exco.ExcelProcessorSpec):
    template = exco.ExcoTemplate.from_excel(
        join(dirname(__file__), '../../sample/test/simple_duplicate_key.xlsx'))
    spec = template.to_raw_excel_processor_spec()
    assert not spec.is_keys_unique()
