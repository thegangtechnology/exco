from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any, List, Optional

from exco import setting as st
from exco.extractor_spec.apv_spec import APVSpec
from exco.extractor_spec.locator_spec import LocatorSpec
from exco.extractor_spec.spec_source import UnknownSource, SpecSource
from exco.extractor_spec.type import SpecParam
from exco.util import name_params


class TableItemDirection(Enum):
    DOWNWARD = 'downward'
    RIGHTWARD = 'rightward'

    @classmethod
    def default(cls) -> 'TableItemDirection':
        return TableItemDirection.DOWNWARD

    @classmethod
    def from_value(cls, v: Optional[str]) -> 'TableItemDirection':
        if v is None:
            return cls.default()
        else:
            return TableItemDirection(v)


Offset = int


@dataclass
class TableEndConditionSpec:
    name: str
    params: SpecParam = field(default_factory=dict)

    @classmethod
    def default_conditions(cls) -> List['TableEndConditionSpec']:
        return [TableEndConditionSpec(name='all_blank', params={})]

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> 'TableEndConditionSpec':
        name, params = name_params[d]
        return TableEndConditionSpec(name=name, params=params)


@dataclass
class ColumnSpecDict:
    offset: int
    dict: Dict[str, Any]
    source: SpecSource


@dataclass
class TableExtractionSpec:
    key: str
    locator: LocatorSpec  # for corner
    columns: Dict[Offset, APVSpec]  # offset -> APVSpec
    end_conditions: List[TableEndConditionSpec] = field(default_factory=TableEndConditionSpec.default_conditions)
    item_direction: TableItemDirection = TableItemDirection.DOWNWARD
    source: SpecSource = field(default_factory=UnknownSource)

    def from_dict(self, d: Dict[str, Any],
                  source: SpecSource,
                  column_dicts: List[ColumnSpecDict]) -> 'TableExtractionSpec':
        """
        Example:

        key: some_key
        locator: {LocatorSpec} # optional
        columns:
            - {offset: offset, spec: {AVPSpec}}
        end_conditions: # optional
            - {EndConditionSpec}
        item_direction: downward # optional

        Args:
            d (Dict[str, Any]):
            source (SpecSource):
            column_dicts (List[ColumnSpecDict])

        Returns:
            TableExtractionSpec
        """
        columns = {
            col.offset: APVSpec.from_dict(d=col.dict, source=col.source)
            for col in column_dicts
        }
        return TableExtractionSpec(
            key=d[st.k_key],
            locator=LocatorSpec.from_dict(d.get(st.k_locator, None)),
            columns=columns,
            end_conditions=[TableEndConditionSpec.from_dict(v) for v in d.get(st.k_end_conditions, [])],
            item_direction=TableItemDirection.from_value(d.get(st.k_item_direction, None))
        )
