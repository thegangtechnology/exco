from unittest.mock import patch

import pytest

from exco.extractor_spec.spec_source import SpecSource, UnknownSource


@patch.multiple(SpecSource, __abstractmethods__=set())
def test_spec_source():
    with pytest.raises(NotImplementedError):
        spec_source = SpecSource()
        spec_source.describe()


def test_unknown_source():
    unknown_source = UnknownSource()
    assert unknown_source.describe() == 'Unknown Source'
