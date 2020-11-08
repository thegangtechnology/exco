import textwrap
from typing import TypeVar, Iterable, Any, Dict, List, Tuple

from openpyxl.utils import get_column_letter

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
    return coordinate_to_tuple(coord)


def shift_coord(coord: str, shift: Tuple[int, int]):
    row, col = coordinate_to_tuple(coord)
    sr, sc = shift
    return tuple_to_coordinate(row + sr, col + sc)


def extra_keys(d: Dict[str, Any], allowed=List[str]) -> List[str]:
    return [k for k in d.keys() if k not in allowed]
