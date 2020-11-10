from os.path import join, dirname

import exco
import pytest
from exco import ExcoTemplate, CellLocation, ExcoBlock
from exco.exception import BadTemplateException
from exco.exco_template.exco_template import ExcoBlockWithLocation


@pytest.fixture
def simple_template() -> exco.ExcoTemplate:
    fname = join(dirname(__file__), '../sample/test/simple.xlsx')
    et = exco.ExcoTemplate.from_excel(fname)
    return et


def test_simple_template(simple_template: exco.ExcoTemplate):
    assert simple_template.n_cell() == 2
    assert simple_template.n_exco_blocks() == 3

    coords = {k.cell_location.coordinate for k in simple_template.cell_blocks}
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


def test_bad_cell_template():
    template = ExcoTemplate(
        table_blocks=[],
        column_blocks=[],
        cell_blocks=[
            ExcoBlockWithLocation(
                cell_location=CellLocation('SHEET1', 'A1'),
                exco_block=ExcoBlock(
                    start_line=1,
                    end_line=3,
                    raw="key: hello\nd:1"  # missing space
                )
            )
        ]
    )
    with pytest.raises(BadTemplateException):
        template.to_excel_extractor_spec()
