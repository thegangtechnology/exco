import exco
from os.path import join, dirname

from exco.extractor.table_end_conditions.table_end_condition_result import TableEndConditionResult


def test_table():
    fname = join(dirname(__file__),
                 '../../sample/test/table/table_template.xlsx')
    template = exco.from_excel(fname)
    result = template.process_excel(fname)

    exp = {'left_table': [
        {'left': 'Hello', 'right': 1},
        {'left': 'world', 'right': 2},
        {'left': 'foo', 'right': 3},
    ]}

    assert result.to_dict() == exp
    assert len(result.table_result_for_key(
        'left_table').result.row_results) == 3


def test_bad_table_end_condition():
    bad = TableEndConditionResult.bad()
    assert not bad.is_ok

    good = TableEndConditionResult.good(False, False)
    assert good.is_ok
