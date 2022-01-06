from dataclasses import asdict
from os.path import join, dirname

import pytest

import exco
from exco.extractor.parser.built_in.link_parser import LinkResult


@pytest.fixture
def template():
    fname = join(dirname(__file__),
                 '../../sample/test/link/link_template.xlsx')
    return exco.from_excel(fname)


def test_good_link(template):
    fname = join(dirname(__file__), '../../sample/test/link/good_link.xlsx')
    result = template.process_excel(fname)
    assert result.to_dict() == {'link': asdict(LinkResult(display="This is the link", link="https://www.google.com/"))}


def test_bad_link(template):
    fname = join(dirname(__file__), '../../sample/test/link/bad_link.xlsx')
    result = template.process_excel(fname)
    assert not result.cell_result_for_key('link').result.is_ok
    assert not result.cell_result_for_key(
        'link').result.parsing_result.is_ok
