from os.path import join, dirname

from excel_comment_orm import ExcelProcessorSpec, ECOTemplate, ExcelProcessorFactory


def test_simple():
    fname = join(dirname(__file__), '../sample/test/simple.xlsx')
    template = ECOTemplate.from_excel(fname)
    spec = template.to_excel_extractor_spec()
    fac = ExcelProcessorFactory.default()
    processor = fac.create_from_spec(spec)

    another_file = join(dirname(__file__), '../sample/test/simple_no_comment.xlsx')
    result = processor.process_excel(another_file)
    assert result.to_dict() == {'random_value': 'hello', 'some_int': 99, 'some_str': '99'}


def test_simple_short_version():
    fname = join(dirname(__file__), '../sample/test/simple.xlsx')
    processor = ExcelProcessorFactory.default().create_from_template_excel(fname)

    another_file = join(dirname(__file__), '../sample/test/simple_no_comment.xlsx')
    result = processor.process_excel(another_file)
    assert result.to_dict() == {'random_value': 'hello', 'some_int': 99, 'some_str': '99'}
