from dataclasses import dataclass
from typing import Dict, Callable

SheetName = str
SheetNameAliasChecker = Callable[[SheetName], bool]
SheetNameAliasCheckers = Dict[SheetName, SheetNameAliasChecker]


@dataclass
class SheetNameAliasChecker:
    sheet_name: str
    checker: Callable[[SheetName], bool]
