import excel_comment_orm as eco
import pytest


def test_from_string():
    comment = eco.util.long_string("""
        %%begin eco
        key: sample_int
        type: int
        %%end eco
        """)

    blocks = eco.ECOBlock.from_string(comment)
    assert len(blocks) == 1
    block = blocks[0]
    assert block.start_line == 1
    assert block.end_line == 4
    exp = """
        key: sample_int
        type: int
        """
    assert block.raw == eco.util.long_string(exp)


def test_from_string_should_throw_double_begin():
    comment = eco.util.long_string("""
        %%begin eco
        %%begin eco
    """)

    with pytest.raises(eco.exception.TooManyBeginException) as exc:
        eco.ECOBlock.from_string(comment)

    assert 'line 2' in str(exc.value)


def test_from_string_should_throw_on_end_before_begin():
    comment = eco.util.long_string("""
        %%end eco
        %%begin eco
    """)

    with pytest.raises(eco.exception.TooManyEndException) as exc:
        eco.ECOBlock.from_string(comment)

    assert 'line 1' in str(exc.value)


def test_from_string_should_throw_on_no_end():
    comment = eco.util.long_string("""
        %%begin eco
        hello
    """)

    with pytest.raises(eco.exception.ExpectEndException) as exc:
        eco.ECOBlock.from_string(comment)

