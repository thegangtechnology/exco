import exco
import pytest
from exco.exco_template.exco_block import ExcoBlockCollection


def test_exco_block_collection():
    comment = exco.util.long_string("""
        {{--table
        key: some_table
        --}}
        {{--col
        table_key: some_table
        key: hello
        parser: int
        --}}
        {{--
        key: some_cell
        parser: string
        --}}
    """)
    ebc = ExcoBlockCollection.from_string(comment)
    assert len(ebc.cell_blocks) == 1
    assert len(ebc.table_blocks) == 1
    assert len(ebc.column_blocks) == 1


def test_from_string():
    comment = exco.util.long_string("""
        {{--
        key: sample_int
        type: int
        --}}
        """)

    blocks = ExcoBlockCollection.from_string(comment)
    assert blocks.n_total_blocks() == 1
    block = blocks.cell_blocks[0]
    assert block.start_line == 1
    assert block.end_line == 3
    exp = """
        key: sample_int
        type: int
        """.rstrip()
    assert block.raw == exco.util.long_string(exp)


def test_from_string_should_throw_double_begin():
    comment = exco.util.long_string("""
        {{--
        {{--
    """)

    with pytest.raises(exco.exception.BadTemplateException) as exc:
        ExcoBlockCollection.from_string(comment)


def test_from_string_should_throw_on_end_before_begin():
    comment = exco.util.long_string("""
        --}}
        {{--
    """)

    with pytest.raises(exco.exception.BadTemplateException) as exc:
        ExcoBlockCollection.from_string(comment)


def test_from_string_should_throw_on_no_end():
    comment = exco.util.long_string("""
        {{--
        hello
    """)

    with pytest.raises(exco.exception.BadTemplateException):
        ExcoBlockCollection.from_string(comment)
