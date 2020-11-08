import exco
import pytest


def test_from_string():
    comment = exco.util.long_string("""
        {{--
        key: sample_int
        type: int
        --}}
        """)

    blocks = exco.ExcoBlock.from_string(comment)
    assert len(blocks) == 1
    block = blocks[0]
    assert block.start_line == 1
    assert block.end_line == 4
    exp = """
        key: sample_int
        type: int
        """
    assert block.raw == exco.util.long_string(exp)


def test_from_string_should_throw_double_begin():
    comment = exco.util.long_string("""
        {{--
        {{--
    """)

    with pytest.raises(exco.exception.TooManyBeginException) as exc:
        exco.ExcoBlock.from_string(comment)

    assert 'line 2' in str(exc.value)


def test_from_string_should_throw_on_end_before_begin():
    comment = exco.util.long_string("""
        --}}
        {{--
    """)

    with pytest.raises(exco.exception.TooManyEndException) as exc:
        exco.ExcoBlock.from_string(comment)

    assert 'line 1' in str(exc.value)


def test_from_string_should_throw_on_no_end():
    comment = exco.util.long_string("""
        {{--
        hello
    """)

    with pytest.raises(exco.exception.ExpectEndException) as exc:
        exco.ExcoBlock.from_string(comment)
