from dataclasses import dataclass, field
from typing import Dict, Any

from exco import util, exception
from exco.extraction_spec.assumption_spec import AssumptionSpec
from exco.extraction_spec.locator_spec import LocatorSpec
from exco.extraction_spec.parser_spec import ParserSpec
from exco.extraction_spec.spec_source import SpecSource, UnknownSource
from exco.extraction_spec.validator_spec import ValidatorSpec


@dataclass
class ExtractionTaskSpec:
    key: str
    parser: ParserSpec
    validations: Dict[str, ValidatorSpec] = field(default_factory=dict)
    assumptions: Dict[str, AssumptionSpec] = field(default_factory=dict)
    source: SpecSource = field(default_factory=UnknownSource)
    locator: LocatorSpec = field(default_factory=LocatorSpec.default)

    @classmethod
    def from_dict(cls, d: Dict[str, Any], source: SpecSource = None) -> 'ExtractionTaskSpec':
        source = source if source is not None else UnknownSource()
        allowed_keys = ['key', 'parser', 'params', 'validations', 'assumptions', 'locator']
        extra_keys = util.extra_keys(d, allowed_keys)
        if extra_keys:
            raise exception.ExcoBlockContainsExtraKey(f'{extra_keys}\n'
                                                     f'allowed_keys are {allowed_keys}')
        return ExtractionTaskSpec(
            key=d['key'],
            parser=ParserSpec.from_dict(d),
            validations={v['key']: ValidatorSpec.from_dict(v) for v in d.get('validations', [])},
            assumptions={v['key']: AssumptionSpec.from_dict(v) for v in d.get('assumptions', [])},
            source=source if source is not None else UnknownSource(),
            locator=LocatorSpec.from_dict(d.get('locator', None))
        )
