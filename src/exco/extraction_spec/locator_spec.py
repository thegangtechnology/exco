from dataclasses import dataclass, field
from typing import Dict, Any, Optional

from exco import setting


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
            return LocatorSpec(name=d['name'],
                               params={k: v for k, v in d.items() if k != 'name'})
