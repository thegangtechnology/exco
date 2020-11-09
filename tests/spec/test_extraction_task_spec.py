import pytest

from exco import ExtractionTaskSpec
from exco.exception import ExcoBlockContainsExtraKey


def test_invalid_extraction_keys():
    with pytest.raises(ExcoBlockContainsExtraKey):
        ExtractionTaskSpec.from_dict(d={
            "key": "test_key",
            "parser": "int",
            "animal": "dog"
        })