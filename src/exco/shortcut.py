from exco import ExcelProcessorFactory, ExcelProcessor
from exco.extractor import Locator, Assumption, Parser, Validator
from exco.extractor.table_end_conditions.table_end_condition import TableEndCondition
from exco.sheet_name_alias import SheetNameAliasCheckers
from typing import Optional, Dict, Type


def from_excel(fname: str,
               sheet_name_checkers: Optional[SheetNameAliasCheckers] = None,
               extra_locators: Optional[Dict[str, Type[Locator]]] = None,
               extra_assumptions: Optional[Dict[str, Type[Assumption]]] = None,
               extra_parsers: Optional[Dict[str, Type[Parser]]] = None,
               extra_validators: Optional[Dict[str, Type[Validator]]] = None,
               extra_table_end_conditions: Optional[Dict[str, Type[TableEndCondition]]] = None,
               accept_only_visible_sheets: bool = False) -> ExcelProcessor:
    """ A shortcut to create excel processor.

    Args:
        fname (str): filename
        sheet_name_checkers (Optional[SheetNameAliasCheckers]): Optional. Default None. sheetname alias checker.
        extra_locators (Optional[Dict[str, Type[Locator]]]): Optional. Default None. Extra locators.
        extra_assumptions (Optional[Dict[str, Type[Assumption]]]): Optional. Default None. Extra Assumptions.
        extra_parsers (Optional[Dict[str, Type[Parser]]]): Optional. Default None. Extra Parsers.
        extra_validators (Optional[Dict[str, Type[Validator]]]): Optional Default None. Extra Validators
        extra_table_end_conditions (Optional[Dict[str, Type[TableEndCondition]]]): Optional.
            Default None. ExtraTableEndCondition.
        accept_only_visible_sheets (bool): true if you want to accept only visible sheets,
            false if you want to accept hidden sheets aswell

    Returns:
        ExcelProcessor.
    """
    fac = ExcelProcessorFactory.default(extra_locators=extra_locators,
                                        extra_assumptions=extra_assumptions,
                                        extra_parsers=extra_parsers,
                                        extra_validators=extra_validators,
                                        extra_table_end_conditions=extra_table_end_conditions)
    return fac.create_from_template_excel(fname=fname,
                                          sheet_name_checkers=sheet_name_checkers,
                                          accept_only_visible_sheets=accept_only_visible_sheets
                                          )
