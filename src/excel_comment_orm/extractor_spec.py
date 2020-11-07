from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any, List

from excel_comment_orm import util, exception, CellLocation
from excel_comment_orm.excel_extraction_scope import ExcelExtractionScope
from excel_comment_orm.spec_source import UnknownSource, SpecSource

SpecParam = Dict[str, Any]


class OnFailEnum(Enum):
    WARN = 'warn'
    ERROR = 'error'


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


@dataclass
class AssumptionTaskSpec:
    """
    Assumption is something to check before parsing
    Ex: if the column on the left has the correct label
    """
    name: str
    params: SpecParam = field(default_factory=dict)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> 'AssumptionTaskSpec':
        """Construct AssumptionTaskSpec

        Args:
            d ():

        Returns:

        """
        params = {k: v for k, v in d.items() if k != 'name'}
        return AssumptionTaskSpec(name=d['name'], params=params)


@dataclass
class ExtractionTaskSpec:
    key: str
    parser: str
    params: SpecParam = field(default_factory=dict)
    validations: List[ValidationTaskSpec] = field(default_factory=list)
    assumptions: List[AssumptionTaskSpec] = field(default_factory=list)
    source: SpecSource = field(default_factory=UnknownSource)

    def from_dict(self, d: Dict[str, Any], source: SpecSource = None) -> 'ExtractionTaskSpec':
        source = source if source is not None else UnknownSource()
        allowed_keys = ['key', 'parser', 'param' 'validations', 'assumptions']
        extra_keys = util.extra_keys(d, allowed_keys)
        if extra_keys:
            raise exception.ECOBlockContainsExtraKey(f'{extra_keys}\n'
                                                     f'allowed_keys are {allowed_keys}')
        return ExtractionTaskSpec(
            key=d['key'],
            parser=d['parser'],
            params=d.get('param', default={}),
            validations=[ValidationTaskSpec.from_dict(v) for v in d.get('validations', default=[])],
            assumptions=[AssumptionTaskSpec.from_dict(v) for v in d.get('assumptions', default=[])],
            source=source if source is not None else UnknownSource()
        )


@dataclass
class ExcelExtractorSpec:
    task_specs: Dict[CellLocation, List[ExtractionTaskSpec]]

    def is_keys_unique(self) -> bool:
        return util.is_unique(spec.key for specs in self.task_specs.values() for spec in specs)
