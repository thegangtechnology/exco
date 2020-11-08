from excel_comment_orm.extraction_spec.parser_spec import ParserSpec
from excel_comment_orm.extractor.parser.parser_factory import ParserFactory


def test_create_simple_spec():
    spec = ParserSpec(name='int')
    fac = ParserFactory.default()
    parser = fac.create_from_spec(spec=spec)
    assert parser.__class__.__name__ == "IntParser"
