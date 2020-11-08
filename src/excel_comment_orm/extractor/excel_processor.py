from dataclasses import dataclass
from typing import TypeVar, Dict, Any, List

import openpyxl
from excel_comment_orm.extraction_spec import ExtractionTaskSpec, ExcelProcessorSpec
from excel_comment_orm.eco_template import ECOTemplate
from excel_comment_orm.cell_location import CellLocation
from excel_comment_orm.exception import ECOException, ExtractionTaskCreationException
from excel_comment_orm.extractor.assumption.assumption_factory import AssumptionFactory
from excel_comment_orm.extractor.extraction_task import ExtractionTaskResult, ExtractionTask
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


@dataclass
class ExcelProcessor:
    processors: Dict[CellLocation, List[ExtractionTask]]

    def process_workbook(self, workbook: Workbook) -> ExcelProcessingResult:
        ret = {}
        for loc, bps in self.processors.items():
            ret[loc] = [bp.process(loc, workbook) for bp in bps]
        return ExcelProcessingResult(ret)

    def process_excel(self, fname: str) -> ExcelProcessingResult:
        wb = openpyxl.load_workbook(fname)
        return self.process_workbook(wb)

    def __str__(self):
        tmp = []
        for cl, tasks in self.processors.items():
            header = f'Location: {cl.short_name}\n'
            sep = '*\n' * 10
            task_str = sep.join([str(task) + '\n' for task in tasks])
            tmp.append(header + task_str)
        ret = ("#" * 20 + '\n').join(tmp)
        return ret


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

    def create_extraction_task(self, spec: ExtractionTaskSpec) -> ExtractionTask:
        try:
            return ExtractionTask(
                key=spec.key,
                locator=self.locator_factory.create_from_spec(spec=spec.locator),
                assumptions={k: self.assumption_factory.create_from_spec(sp) for k, sp in
                             spec.assumptions.items()},
                parser=self.parser_factory.create_from_spec(spec=spec.parser),
                validators={k: self.validator_factory.create_from_spec(sp) for k, sp in
                            spec.validations.items()}
            )
        except ECOException as e:
            raise ExtractionTaskCreationException(
                f'Unable to create ExtractionTask for {spec.key} cf {spec.source.describe()}') from e

    def create_from_spec(self, spec: ExcelProcessorSpec) -> ExcelProcessor:
        ret = {}
        for cl, specs in spec.task_specs.items():
            tmp = []
            for spec in specs:
                tmp.append(self.create_extraction_task(spec))
            ret[cl] = tmp
        return ExcelProcessor(ret)

    def create_from_template_excel(self, fname: str) -> ExcelProcessor:
        workbook = openpyxl.load_workbook(fname)
        return self.create_from_template_workbook(workbook)

    def create_from_template_workbook(self, workbook: Workbook) -> ExcelProcessor:
        template = ECOTemplate.from_workbook(workbook)
        spec = template.to_excel_extractor_spec()
        return self.create_from_spec(spec)
