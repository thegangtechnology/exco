from exco import util


def test_long_string():
    s = """
    hello
    world
    """
    assert util.long_string(s) == "hello\nworld\n"


def test_remove_suffix():
    s = "hello.com"
    assert util.remove_suffix(s, '.com') == 'hello'

    s = "hello.com"
    assert util.remove_suffix(s, 'abc') == 'hello.com'


class HelloParser:
    pass


class IntWithOffsetParser:
    pass


def test_default_key():
    assert util.default_key(HelloParser, 'Parser') == 'hello'
    assert util.default_key(IntWithOffsetParser, 'Parser') == 'int_with_offset'
