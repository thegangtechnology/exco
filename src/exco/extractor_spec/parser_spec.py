from dataclasses import dataclass, field
from typing import Dict, Any, ClassVar, Set

from exco.exception import ExcoException, ParserSpecCreationException
from exco.extractor_spec.type import SpecParam

from exco import setting as st


@dataclass
class ParserSpec:
    name: str
    params: SpecParam = field(default_factory=dict)

    allowed_keys: ClassVar[Set[str]] = {st.k_parser, st.k_params}

    @classmethod
    def from_dict(cls, d: Dict[str, Any]):
        try:
            return ParserSpec(
                name=d[st.k_parser],
                params=d.get(st.k_params, {})
            )
        except (ExcoException, KeyError) as e:
            raise ParserSpecCreationException(f'Can\'t create parser from {d}') from e
