from os.path import join, dirname

import exco


def test_deref():
    template = join(dirname(__file__), '../sample/test/simple_deref.xlsx')
    processor = exco.from_excel(template)
    data = join(dirname(__file__), '../sample/test/simple_deref_to_extract.xlsx')
    result = processor.process_excel(data)
    assert result.to_dict() == {
        'deref_key': 12,
        'world': 34
    }
