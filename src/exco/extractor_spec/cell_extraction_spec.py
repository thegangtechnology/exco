from dataclasses import dataclass, field
from typing import Dict, Any, ClassVar, Set, TypeVar, Generic

from exco import setting as st
from exco import util, exception
from exco.dereferator import Dereferator
from exco.extractor_spec.apv_spec import APVSpec
from exco.extractor_spec.assumption_spec import AssumptionSpec
from exco.extractor_spec.locator_spec import LocatorSpec
from exco.extractor_spec.parser_spec import ParserSpec
from exco.extractor_spec.spec_source import SpecSource, UnknownSource
from exco.extractor_spec.validator_spec import ValidatorSpec

T = TypeVar('T')


@dataclass
class CellExtractionSpec(Generic[T]):
    apv: APVSpec
    locator: LocatorSpec = field(default_factory=LocatorSpec.default)
    source: SpecSource = field(default_factory=UnknownSource)

    consumed_keys: ClassVar[Set[str]] = {st.k_locator, st.k_fallback}
    allowed_keys: ClassVar[Set[str]] = consumed_keys | APVSpec.allowed_keys

    def deref(self, dereferator: Dereferator) -> 'CellExtractionSpec':
        """Create a new copy with <<A1>> and such derefed with value in the workbook
        Args:
            dereferator ():

        Returns:
            A new copy of cell extraction spec.
        """
        return CellExtractionSpec(
            apv=self.apv.deref(dereferator),
            locator=self.locator.deref(dereferator),
            source=self.source
        )

    @property
    def key(self) -> str:
        return self.apv.key

    @property
    def parser(self) -> ParserSpec:
        return self.apv.parser

    @property
    def validations(self) -> Dict[str, ValidatorSpec]:
        return self.apv.validations

    @property
    def assumptions(self) -> Dict[str, AssumptionSpec]:
        return self.apv.assumptions

    @property
    def fallback(self) -> T:
        return self.apv.fallback

    @classmethod
    def from_dict(cls, d: Dict[str, Any],
                  source: SpecSource = None) -> 'CellExtractionSpec':
        source = source if source is not None else UnknownSource()
        extra_keys = util.extra_keys(d, cls.allowed_keys)
        if extra_keys:
            raise exception.ExcoBlockContainsExtraKey(
                f'{extra_keys}\n' + f'allowed_keys are {cls.allowed_keys}')
        return CellExtractionSpec(
            locator=LocatorSpec.from_dict(d.get(st.k_locator, None)),
            apv=APVSpec.from_dict(d, source),
            source=source,
        )
