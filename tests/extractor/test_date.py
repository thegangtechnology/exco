import pytest
from os.path import join, dirname
import exco
from datetime import date


@pytest.fixture
def template():
    fname = join(dirname(__file__),
                 '../../sample/test/date/date_template.xlsx')
    return exco.from_excel(fname)


def test_good_date(template):
    fname = join(dirname(__file__), '../../sample/test/date/good_date.xlsx')
    result = template.process_excel(fname)
    assert result.to_dict() == {'some_date': date(2021, 3, 2)}


def test_bad_date(template):
    fname = join(dirname(__file__), '../../sample/test/date/bad_date.xlsx')
    result = template.process_excel(fname)
    assert not result.cell_result_for_key('some_date').result.is_ok
    assert not result.cell_result_for_key(
        'some_date').result.parsing_result.is_ok
