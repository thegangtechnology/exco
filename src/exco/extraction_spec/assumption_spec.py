from dataclasses import dataclass, field
from typing import Dict, Any

from exco.extraction_spec.type import SpecParam


@dataclass
class AssumptionSpec:
    """
    Assumption is something to check before parsing
    Ex: if the column on the left has the correct label
    """
    name: str
    params: SpecParam = field(default_factory=dict)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> 'AssumptionSpec':
        """Construct AssumptionTaskSpec

        Args:
            d ():

        Returns:

        """
        params = {k: v for k, v in d.items() if k != 'name'}
        return AssumptionSpec(name=d['name'], params=params)
