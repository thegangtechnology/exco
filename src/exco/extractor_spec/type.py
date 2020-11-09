from enum import Enum
from typing import Dict, Any

SpecParam = Dict[str, Any]


class OnFailEnum(Enum):
    WARN = 'warn'
    ERROR = 'error'
