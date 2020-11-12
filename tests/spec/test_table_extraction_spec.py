from typing import Dict, Any

import pytest
from exco.extractor_spec.table_extraction_spec import TableItemDirection, TableEndConditionSpec, TableExtractionSpec


def test_from_value():
    assert TableItemDirection.from_value(
        'downward') == TableItemDirection.DOWNWARD
    assert TableItemDirection.from_value(
        'rightward') == TableItemDirection.RIGHTWARD
    assert TableItemDirection.from_value(None) == TableItemDirection.default()


def test_table_end_condition_spec():
    spec = TableEndConditionSpec.from_dict(
        {'name': 'max_row', 'n': 5}
    )
    assert spec.name == 'max_row'
    assert spec.params == {'n': 5}


@pytest.fixture(scope='function')
def full_table_spec_dict() -> Dict[str, Any]:
    return {
        'key': 'some_table',
        'locator': {'name': 'at_comment_cell'},
        'end_conditions': [
            {'name': 'max_row', 'n': 5},
            {'name': 'all_blank'}
        ],
        'columns': {
            1: {'key': 'col2', 'parser': 'int'},
            2: {'key': 'col2', 'parser': 'string'}
        },
        'item_direction': 'downward'
    }


def test_table_extraction_spec(full_table_spec_dict: Dict[str, Any]):
    spec = TableExtractionSpec.from_dict(full_table_spec_dict)

    assert spec.key == 'some_table'
    assert len(spec.end_conditions) == 2
    assert len(spec.columns) == 2
    assert spec.item_direction == TableItemDirection.DOWNWARD


def test_table_extraction_spec_no_end_conditions(full_table_spec_dict: Dict[str, Any]):
    full_table_spec_dict.pop('end_conditions')
    spec = TableExtractionSpec.from_dict(full_table_spec_dict)

    assert spec.key == 'some_table'
    assert len(spec.end_conditions) == 1  # automatically filled
    assert spec.end_conditions[0].name == 'all_blank'
    assert len(spec.columns) == 2
    assert spec.item_direction == TableItemDirection.DOWNWARD
