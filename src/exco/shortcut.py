from exco import ExcelProcessorFactory
from exco.sheet_name_alias import SheetNameAliasCheckers
from typing import Optional


def from_excel(fname: str, sheet_name_checkers: Optional[SheetNameAliasCheckers] = None):
    return ExcelProcessorFactory.default().create_from_template_excel(fname=fname,
                                                                      sheet_name_checkers=sheet_name_checkers
                                                                      )
