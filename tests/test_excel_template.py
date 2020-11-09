from os.path import join, dirname

import exco
import pytest


@pytest.fixture
def simple_template() -> exco.ExcoTemplate:
    fname = join(dirname(__file__), '../sample/test/simple.xlsx')
    et = exco.ExcoTemplate.from_excel(fname)
    return et


def test_simple_template(simple_template: exco.ExcoTemplate):
    assert simple_template.n_cell() == 2
    assert simple_template.n_exco_blocks() == 3

    coords = {k.coordinate for k in simple_template.exco_blocks.keys()}
    assert coords == {'B5', 'D2'}


def test_bad_template():
    fname = join(dirname(__file__), '../sample/test/bad_template.xlsx')
    with pytest.raises(exco.exception.BadTemplateException):
        exco.ExcoTemplate.from_excel(fname)


def test_questionable_template():
    fname = join(dirname(__file__), '../sample/test/questionable.xlsx')
    with pytest.raises(exco.exception.CommentWithNoExcoBlockWarning) as exc:
        exco.ExcoTemplate.from_excel(fname)
    assert "B8" in str(exc.value)
