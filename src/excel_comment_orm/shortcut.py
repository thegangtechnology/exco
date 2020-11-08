from excel_comment_orm import ExcelProcessorFactory


def from_excel(fname: str):
    return ExcelProcessorFactory.default().create_from_template_excel(fname)
