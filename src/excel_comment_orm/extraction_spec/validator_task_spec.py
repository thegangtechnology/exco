from dataclasses import dataclass, field
from typing import Dict, Any

from excel_comment_orm.extraction_spec.type import SpecParam


@dataclass
class ValidationTaskSpec:
    """
    Validation is something to check after parsing
    Ex: if the parsed value is greater than 99
    # TODO: Maybe I should put a source here too
    """
    name: str
    params: SpecParam = field(default_factory=dict)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> 'ValidationTaskSpec':
        """Construct ValidationTaskSpec from dict
        {name: greater_than, threshold: 99}

        Args:
            d (Dict[str, Any]):

        Returns:
            ValidationTaskSpec
        """
        params = {k: v for k, v in d.items() if k != 'name'}
        return ValidationTaskSpec(name=d['name'], params=params)
