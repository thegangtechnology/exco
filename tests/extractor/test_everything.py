from os.path import join, dirname

import exco
import datetime


def test_everything():
    fname = join(dirname(__file__), '../../sample/test/everything/everything_template.xlsx')
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
