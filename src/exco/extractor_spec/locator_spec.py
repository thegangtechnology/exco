from dataclasses import dataclass, field
from typing import Dict, Any, Optional

from exco import setting
from exco.util import name_params


@dataclass
class LocatorSpec:
    name: str
    params: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def default(cls):
        return LocatorSpec(name=setting.default_locator)

    @classmethod
    def from_dict(cls, d: Optional[Dict[str, Any]]) -> 'LocatorSpec':
        if d is None:
            return cls.default()
        else:
            name, params = name_params(d)
            return LocatorSpec(name=name, params=params)
