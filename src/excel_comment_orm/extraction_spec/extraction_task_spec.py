from dataclasses import dataclass, field
from typing import List, Dict, Any

from excel_comment_orm import util, exception
from excel_comment_orm.extraction_spec.assumption_task_spec import AssumptionTaskSpec
from excel_comment_orm.extraction_spec.locator_spec import LocatorSpec
from excel_comment_orm.extraction_spec.spec_source import SpecSource, UnknownSource
from excel_comment_orm.extraction_spec.type import SpecParam
from excel_comment_orm.extraction_spec.validator_task_spec import ValidationTaskSpec


@dataclass
class ExtractionTaskSpec:
    key: str
    parser: str
    params: SpecParam = field(default_factory=dict)
    validations: List[ValidationTaskSpec] = field(default_factory=list)
    assumptions: List[AssumptionTaskSpec] = field(default_factory=list)
    source: SpecSource = field(default_factory=UnknownSource)
    locator: LocatorSpec = field(default_factory=LocatorSpec.default)

    @classmethod
    def from_dict(cls, d: Dict[str, Any], source: SpecSource = None) -> 'ExtractionTaskSpec':
        source = source if source is not None else UnknownSource()
        allowed_keys = ['key', 'parser', 'params', 'validations', 'assumptions', 'locator']
        extra_keys = util.extra_keys(d, allowed_keys)
        if extra_keys:
            raise exception.ECOBlockContainsExtraKey(f'{extra_keys}\n'
                                                     f'allowed_keys are {allowed_keys}')
        return ExtractionTaskSpec(
            key=d['key'],
            parser=d['parser'],
            params=d.get('params', {}),
            validations=[ValidationTaskSpec.from_dict(v) for v in d.get('validations', [])],
            assumptions=[AssumptionTaskSpec.from_dict(v) for v in d.get('assumptions', [])],
            source=source if source is not None else UnknownSource(),
            locator=LocatorSpec.from_dict(d.get('locator', None))
        )
