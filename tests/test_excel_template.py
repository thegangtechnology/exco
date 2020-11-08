from os.path import join, dirname

import excel_comment_orm as eco
import pytest


@pytest.fixture
def simple_template() -> eco.ECOTemplate:
    fname = join(dirname(__file__), '../sample/test/simple.xlsx')
    et = eco.ECOTemplate.from_excel(fname)
    return et


def test_simple_template(simple_template: eco.ECOTemplate):
    assert simple_template.n_cell() == 2
    assert simple_template.n_eco_blocks() == 3

    coords = {k.coordinate for k in simple_template.eco_blocks.keys()}
    assert coords == {'B5', 'D2'}


def test_bad_template():
    fname = join(dirname(__file__), '../sample/test/bad_template.xlsx')
    with pytest.raises(eco.exception.BadTemplateException) as exc:
        eco.ECOTemplate.from_excel(fname)


def test_questionable_template():
    fname = join(dirname(__file__), '../sample/test/questionable.xlsx')
    with pytest.raises(eco.exception.CommentWithNoECOBlockWarning) as exc:
        et = eco.ECOTemplate.from_excel(fname)
    assert "B8" in str(exc.value)
