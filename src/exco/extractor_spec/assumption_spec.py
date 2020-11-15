from dataclasses import dataclass, field
from typing import Dict, Any

from exco.dereferator import Dereferator
from exco.extractor_spec.type import SpecParam
from exco.util import name_params


@dataclass
class AssumptionSpec:
    """
    Assumption is something to check before parsing
    Ex: if the column on the left has the correct label
    """
    name: str
    params: SpecParam = field(default_factory=dict)

    def deref(self, dereferator: Dereferator) -> 'AssumptionSpec':
        return AssumptionSpec(
            name=dereferator.deref_text(self.name),
            params={k: dereferator.deref_text(v) for k, v in self.params.items()}
        )

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> 'AssumptionSpec':
        """Construct AssumptionTaskSpec

        Args:
            d ():

        Returns:

        """
        name, params = name_params(d)
        return AssumptionSpec(name=name, params=params)
