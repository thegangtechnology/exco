from dataclasses import dataclass, field
from typing import Dict, Any, Optional

from exco import setting


@dataclass
class DerefSpec:
    name: str
    params: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def default(cls):
        return DerefSpec(name=setting.default_deref)

    @classmethod
    def from_dict(cls, d: Optional[Dict[str, Any]]) -> 'DerefSpec':
        if d is None:
            return cls.default()
        elif isinstance(d, bool) and d is False:
            return DerefSpec(name='no')
        else:
            return DerefSpec(name=d)
