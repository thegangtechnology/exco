import pytest

from exco import CellExtractionSpec
from exco.exception import ExcoBlockContainsExtraKey


def test_invalid_extraction_keys():
    with pytest.raises(ExcoBlockContainsExtraKey):
        CellExtractionSpec.from_dict(d={
            "key": "test_key",
            "parser": "int",
            "animal": "dog"
        })
