import pytest
from openpyxl import Workbook
from openpyxl.comments import Comment


@pytest.fixture
def workbook() -> Workbook:
    wb = Workbook()
    sheet = wb.active
    sheet['A1'].comment = Comment(
        'hello', author='me'
    )

    sheet['A2'].comment = Comment(
        'bye', author='you'
    )
    return wb
