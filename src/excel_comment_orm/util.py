import textwrap
from typing import TypeVar, Iterable, Any, Dict, List

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


def extra_keys(d: Dict[str, Any], allowed=List[str]) -> List[str]:
    return [k for k in d.keys() if k not in allowed]
