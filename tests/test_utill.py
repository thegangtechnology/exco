from excel_comment_orm import util

def test_long_string():
    s = """
    hello
    world
    """
    assert util.long_string(s) == "hello\nworld\n"
