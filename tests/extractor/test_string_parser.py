from exco.extractor.parser.built_in.string_parser import StringParser


def test_string_parser_should_return_empty_string_on_empty_cell():
    sp = StringParser()
    assert sp.parse_value(None) == ''


def test_string_parser_simple():
    sp = StringParser()
    assert sp.parse_value('hello') == 'hello'
