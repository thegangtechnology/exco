import textwrap
from collections import defaultdict
from typing import TypeVar, Iterable, Any, Dict, List, Tuple, Type, Set, Optional, Generator, Sequence, Callable

import openpyxl
from exco.cell_full_path import CellFullPath
from openpyxl import Workbook
from openpyxl.cell import Cell

from openpyxl.utils import get_column_letter
import stringcase
from exco import setting as st
import itertools

from openpyxl.worksheet.worksheet import Worksheet

T = TypeVar('T')


def long_string(s: str) -> str:
    """left strip and dedent the string

    Args:
        s (str):

    Returns:
        left string and dedent the string
    """
    return textwrap.dedent(s).lstrip()


def is_unique(items: Iterable[Any]) -> bool:
    s = set()
    for item in items:
        if item in s:
            return False
        s.add(item)
    return True


def tuple_to_coordinate(row, col) -> str:
    return get_column_letter(col) + str(row)


def coordinate_to_tuple(coord: str) -> Tuple[int, int]:
    return openpyxl.utils.coordinate_to_tuple(coord)


def shift_coord(coord: str, shift: Tuple[int, int]):
    row, col = coordinate_to_tuple(coord)
    sr, sc = shift
    return tuple_to_coordinate(row + sr, col + sc)


def remove_suffix(s: str, suffix: str):  # polyfill for python<3.9
    """Remove suffix(if exists) from s

    Args:
        s (str):
        suffix (str): suffix to remove.

    Returns:
        suffix removed s.
    """
    if s.endswith(suffix):
        return s[:-len(suffix)]
    else:
        return s


def default_key(clz: Type[Any], suffix):
    """Return snake case with suffix removed. This is used as default key for class.

    Args:
        s (str):
        suffix (str):

    Returns:
        default key name: Ex: IntParser -> int

    """
    return stringcase.snakecase(remove_suffix(clz.__name__, suffix))


def extra_keys(d: Dict[str, Any], allowed=Set[str]) -> List[str]:
    return [k for k in d.keys() if k not in allowed]


def name_params(d: Dict[str, Any], exclude: Optional[Set[str]] = None) -> Tuple[str, Dict[str, Any]]:
    exclude = set() if exclude is None else exclude
    name = d[st.k_name]
    params = {k: v for k, v in d.items() if k != st.k_name and k not in exclude}
    return name, params


def flatten(lol: Iterable[Iterable[T]]) -> Iterable[T]:
    return itertools.chain.from_iterable(lol)


def flattened_len(it: Iterable[Iterable]):
    """Find the len of flatten list
    """
    return sum(1 for _ in flatten(it))


def iterate_cells_in_worksheet(sheet: Worksheet) -> Generator[Cell, None, None]:
    for row in sheet.iter_rows():
        for cell in row:
            yield cell


def iterate_cells_in_workbook(workbook: Workbook) -> Generator[CellFullPath, None, None]:
    for sheetname in workbook.sheetnames:
        sheet: Worksheet = workbook[sheetname]
        for cell in iterate_cells_in_worksheet(sheet):
            yield CellFullPath(
                workbook=workbook,
                sheetname=sheetname,
                sheet=sheet,
                cell=cell)


def unique(xs: Iterable[T]) -> List[T]:
    return list(set(xs))


T2 = TypeVar('T2')


def group_by(f: Callable[[T], T2], xs: List[T]) -> Dict[T2, List[T]]:
    ret = defaultdict(list)
    for x in xs:
        key = f(x)
        ret[key].append(x)
    return dict(ret)
