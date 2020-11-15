from dataclasses import dataclass, field
from typing import Dict, Any, Optional

from exco import setting
from exco.dereferator import Dereferator
from exco.extractor_spec.type import SpecParam
from exco.util import name_params


@dataclass
class LocatorSpec:
    name: str
    params: SpecParam = field(default_factory=dict)

    def deref(self, dereferator: Dereferator) -> 'LocatorSpec':
        return LocatorSpec(
            name=dereferator.deref_text(self.name),
            params={k: dereferator.deref_text(v) for k, v in self.params.items()}
        )

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
