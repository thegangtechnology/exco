from dataclasses import dataclass, field
from typing import Dict, Any

from exco.extraction_spec.type import SpecParam


@dataclass
class ParserSpec:
    name: str
    params: SpecParam = field(default_factory=dict)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]):
        return ParserSpec(
            name=d['parser'],
            params=d.get('params', {})
        )
