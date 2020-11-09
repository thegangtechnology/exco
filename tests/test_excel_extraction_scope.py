from unittest.mock import patch

import pytest

from exco.excel_extraction_scope import ExcelExtractionScope


@patch.multiple(ExcelExtractionScope, __abstractmethods__=set())
def test_get_cell_full_path_abstract():
    with pytest.raises(NotImplementedError):
        excel_extraction_scope = ExcelExtractionScope()
        excel_extraction_scope.get_cell_full_path([])
