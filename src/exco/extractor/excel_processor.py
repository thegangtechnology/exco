from dataclasses import dataclass
from typing import TypeVar, Dict, Any, List, Optional, Generic

import openpyxl
from exco.cell_location import CellLocation
from exco.exception import ExcoException, ExtractionTaskCreationException, TableExtractionTaskCreationException
from exco.exco_template import ExcoTemplate
from exco.extractor.assumption.assumption_factory import AssumptionFactory
from exco.extractor.cell_extraction_task import CellExtractionTaskResult, CellExtractionTask
from exco.extractor.locator.locator_factory import LocatorFactory
from exco.extractor.parser.parser_factory import ParserFactory
from exco.extractor.table_end_conditions.table_end_condition_factory import TableEndConditionFactory
from exco.extractor.table_extraction_task import TableExtractionTask, EndConditionCollection, TableExtractionTaskResult
from exco.extractor.validator.validator_factory import ValidatorFactory
from exco.extractor_spec import CellExtractionSpec, ExcelProcessorSpec
from exco.extractor_spec.table_extraction_spec import TableExtractionSpec
from openpyxl import Workbook

T = TypeVar('T')


@dataclass
class ProcessorKey:
    cell_location: CellLocation
    key: str

    def __hash__(self):
        return hash((self.cell_location, self.key))


@dataclass
class LookupResult(Generic[T]):
    cell_location: CellLocation
    result: T


@dataclass
class ExcelProcessingResult:
    cell_results: Dict[CellLocation, List[CellExtractionTaskResult]]
    table_results: Dict[CellLocation, List[TableExtractionTaskResult]]

    @property
    def is_ok(self):
        return all(cr.is_ok for crs in self.cell_results.values() for cr in crs) and \
               all(tr.is_ok for trs in self.table_results.values() for tr in trs)

    def _lookup_for_key(self, d: Dict[CellLocation, List[T]], key: str) -> Optional[LookupResult[T]]:
        for cl, results in d.items():
            for result in results:
                if key == result.key:
                    return LookupResult(cl, result)
            # TODO: Fix this O(n) search.
        return None

    def cell_result_for_key(self, key: str) -> Optional[LookupResult[CellExtractionTaskResult]]:
        return self._lookup_for_key(self.cell_results, key)

    def table_result_for_key(self, key: str) -> Optional[LookupResult[TableExtractionTaskResult]]:
        return self._lookup_for_key(self.table_results, key)

    def to_dict(self) -> Dict[str, Any]:
        ret = {}
        for results in self.cell_results.values():  # TODO: Warn of duplicate key
            for result in results:
                ret[result.key] = result.get_value(None)

        for results in self.table_results.values():  # TODO: Warn of duplicate key
            for result in results:
                ret[result.key] = result.get_value()
        return ret


@dataclass
class ExcelProcessor:
    cell_processors: Dict[CellLocation, List[CellExtractionTask]]
    table_processors: Dict[CellLocation, List[TableExtractionTask]]

    def process_workbook(self, workbook: Workbook) -> ExcelProcessingResult:
        cell_result = {}
        for loc, cets in self.cell_processors.items():
            cell_result[loc] = [cet.process(loc, workbook) for cet in cets]

        table_result = {}
        for loc, tets in self.table_processors.items():
            table_result[loc] = [tet.process(loc, workbook) for tet in tets]
        return ExcelProcessingResult(cell_results=cell_result, table_results=table_result)

    def process_excel(self, fname: str) -> ExcelProcessingResult:
        wb = openpyxl.load_workbook(fname)
        return self.process_workbook(wb)

    def __str__(self):
        tmp = []
        for cl, tasks in self.cell_processors.items():
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
    table_end_condition_factory: TableEndConditionFactory

    @classmethod
    def default(cls):
        return ExcelProcessorFactory(
            locator_factory=LocatorFactory.default(),
            assumption_factory=AssumptionFactory.default(),
            parser_factory=ParserFactory.default(),
            validator_factory=ValidatorFactory.default(),
            table_end_condition_factory=TableEndConditionFactory.default()
        )

    def create_extraction_task(self, spec: CellExtractionSpec) -> CellExtractionTask:
        try:
            return CellExtractionTask(
                key=spec.key,
                locator=self.locator_factory.create_from_spec(spec=spec.locator),
                assumptions={k: self.assumption_factory.create_from_spec(sp) for k, sp in
                             spec.assumptions.items()},
                parser=self.parser_factory.create_from_spec(spec=spec.parser),
                validators={k: self.validator_factory.create_from_spec(sp) for k, sp in
                            spec.validations.items()}
            )
        except ExcoException as e:
            raise ExtractionTaskCreationException(
                f'Unable to create ExtractionTask for {spec.key} cf {spec.source.describe()}') from e

    def create_table_extraction_task(self, spec: TableExtractionSpec) -> TableExtractionTask:
        columns = {k: self.create_extraction_task(CellExtractionSpec(v))
                   for k, v in spec.columns.items()}
        try:
            return TableExtractionTask(
                key=spec.key,
                locator=self.locator_factory.create_from_spec(spec=spec.locator),
                columns=columns,
                end_condition=EndConditionCollection.from_spec(spec.end_conditions,
                                                               factory=self.table_end_condition_factory),
                item_direction=spec.item_direction
            )
        except ExcoException as e:
            raise TableExtractionTaskCreationException(
                f'Unable to create TableExtractionTask for {spec.key} cf\n {spec.source.describe()}') from e

    def create_from_spec(self, spec: ExcelProcessorSpec) -> ExcelProcessor:
        cell_tasks = {}
        for cl, specs in spec.cell_specs.items():
            cell_tasks[cl] = [self.create_extraction_task(spec) for spec in specs]

        table_tasks = {}
        for cl, specs in spec.table_specs.items():
            table_tasks[cl] = [self.create_table_extraction_task(spec) for spec in specs]

        return ExcelProcessor(cell_processors=cell_tasks, table_processors=table_tasks)

    def create_from_template_excel(self, fname: str) -> ExcelProcessor:
        workbook = openpyxl.load_workbook(fname)
        return self.create_from_template_workbook(workbook)

    def create_from_template_workbook(self, workbook: Workbook) -> ExcelProcessor:
        template = ExcoTemplate.from_workbook(workbook)
        spec = template.to_excel_extractor_spec()
        return self.create_from_spec(spec)
