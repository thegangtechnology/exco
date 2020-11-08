from dataclasses import dataclass, field
from typing import Dict, Any

from exco.extraction_spec.type import SpecParam


@dataclass
class ValidatorSpec:
    """
    Validation is something to check after parsing
    Ex: if the parsed value is greater than 99
    # TODO: Maybe I should put a source here too
    """
    name: str
    params: SpecParam = field(default_factory=dict)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> 'ValidatorSpec':
        """Construct ValidationTaskSpec from dict
        {name: greater_than, threshold: 99}

        Args:
            d (Dict[str, Any]):

        Returns:
            ValidationTaskSpec
        """
        params = {k: v for k, v in d.items() if k not in ['name', 'key']}
        return ValidatorSpec(name=d['name'], params=params)
