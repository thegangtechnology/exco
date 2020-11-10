import exco
from os.path import join, dirname


def test_table():
    fname = join(dirname(__file__), '../../sample/test/table/table_template.xlsx')
    template = exco.from_excel(fname)
    result = template.process_excel(fname)

    exp = {'left_table': [
        {'left': 'Hello', 'right': 1},
        {'left': 'world', 'right': 2},
        {'left': 'foo', 'right': 3},
    ]}

    assert result.to_dict() == exp
