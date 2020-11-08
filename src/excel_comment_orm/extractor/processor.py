from dataclasses import dataclass
from typing import TypeVar, Dict, Any, List

import openpyxl
from excel_comment_orm import ExtractionTaskSpec
from excel_comment_orm.cell_full_path import CellFullPath
from excel_comment_orm.cell_location import CellLocation
from excel_comment_orm.exception import ECOException, ExtractionTaskCreationException
from excel_comment_orm.extractor.assumption.assumption_factory import AssumptionFactory
from excel_comment_orm.extractor.block_processor import ExtractionTaskResult, ExtractionTask
from excel_comment_orm.extractor.locator.locator_factory import LocatorFactory
from excel_comment_orm.extractor.parser.parser_factory import ParserFactory
from excel_comment_orm.extractor.validator.validator_factory import ValidatorFactory
from openpyxl import Workbook

T = TypeVar('T')


@dataclass
class ProcessorKey:
    cell_location: CellLocation
    key: str

    def __hash__(self):
        return hash((self.cell_location, self.key))


@dataclass
class ExcelProcessingResult:
    results: Dict[CellLocation, List[ExtractionTaskResult]]

    def to_dict(self) -> Dict[str, Any]:
        ret = {}
        for results in self.results.values():  # TODO: Warn of duplicate key
            for result in results:
                ret[result.key] = result.get_value(None)
        return ret


class ExcelProcessor:
    processors: Dict[CellLocation, List[ExtractionTask]]

    def process_workbook(self, workbook: Workbook) -> ExcelProcessingResult:
        ret = {}
        for loc, bps in self.processors.items():
            ret[loc] = [bp.process(loc, workbook) for bp in bps]
        return ExcelProcessingResult(ret)

    def process_file(self, fname: str) -> ExcelProcessingResult:
        wb = openpyxl.load_workbook(fname)
        return self.process_workbook(wb)


@dataclass
class ExcelProcessorFactory:
    locator_factory: LocatorFactory
    assumption_factory: AssumptionFactory
    parser_factory: ParserFactory
    validator_factory: ValidatorFactory

    @classmethod
    def default(cls):
        return ExcelProcessorFactory(
            locator_factory=LocatorFactory.default(),
            assumption_factory=AssumptionFactory.default(),
            parser_factory=ParserFactory.default(),
            validator_factory=ValidatorFactory.default()
        )

    def create_extraction_task(self, cfp: CellFullPath, spec: ExtractionTaskSpec) -> ExtractionTask:
        try:
            return ExtractionTask(
                key=spec.key,
                locator=self.locator_factory.create_from_spec(cfp, spec=spec.locator),
                assumptions={k: self.assumption_factory.create_from_spec(cfp, sp) for k, sp in
                             spec.assumptions.items()},
                parser=self.parser_factory.create_from_spec(cfp, spec=spec.parser),
                validators={k: self.validator_factory.create_from_spec(cfp, sp) for k, sp in
                            spec.validations.items()}
            )
        except ECOException as e:
            raise ExtractionTaskCreationException(
                f'Unable to create ExtractionTask for {spec.key} cf {spec.source.describe()}') from e
