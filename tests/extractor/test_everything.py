import datetime
from os.path import join, dirname

import exco
from exco import ExcoTemplate

fname = join(dirname(__file__),
             '../../sample/test/everything/everything_template.xlsx')


def test_everything():
    template = exco.from_excel(fname)
    result = template.process_excel(fname)

    exp = {'left_table': [{'left': 'Hello', 'right': 1},
                          {'left': 'world', 'right': 2},
                          {'left': 'foo', 'right': 3}],
           'right_table': [{'left': 'aaa', 'right': 1},
                           {'left': 'bbb', 'right': 2},
                           {'left': 'ccc', 'right': 3}],
           'some_date': datetime.date(1982, 8, 23),
           'some_float': 1.23,
           'some_int': 1,
           'some_string': 'string'}

    assert result.to_dict() == exp
    assert result.is_ok


def test_everything_spec():
    template = ExcoTemplate.from_excel(fname)
    spec = template.to_raw_excel_processor_spec()

    assert spec.n_table_spec() == 2
    assert spec.n_cell_spec() == 4
    assert spec.n_table_location() == 2
    assert spec.n_cell_location() == 4
    assert spec.n_total_location() == 6
    assert spec.n_total_spec() == 6
