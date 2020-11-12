from os.path import join, dirname
import exco

import pytest


@pytest.fixture
def template() -> exco.ExcelProcessor:
    template_name = join(
        dirname(__file__), '../../sample/test/validation/validation_template.xlsx')
    return exco.from_excel(template_name)


def test_with_good_result(template: exco.ExcelProcessor):
    good_excel = join(dirname(__file__),
                      '../../sample/test/validation/good_validation_data.xlsx')
    good_result = template.process_excel(good_excel)

    task_result = good_result.cell_result_for_key('some_value').result
    assert task_result.validation_results['between'].is_ok
    assert good_result.to_dict() == {'some_value': 2}


def test_with_bad_result(template: exco.ExcelProcessor):
    bad_excel = join(dirname(__file__),
                     '../../sample/test/validation/bad_validation_data.xlsx')
    bad_result = template.process_excel(bad_excel)
    task_result = bad_result.cell_result_for_key('some_value').result
    assert not task_result.validation_results['between'].is_ok

    assert not task_result.is_ok
