from dataclasses import dataclass
from itertools import chain
from typing import Dict, List, Callable

from exco import util
from exco.cell_location import CellLocation
from exco.dereferator import Dereferator
from exco.extractor_spec.cell_extraction_spec import CellExtractionSpec
from exco.extractor_spec.table_extraction_spec import TableExtractionSpec
from openpyxl import Workbook, load_workbook


@dataclass
class ExcelProcessorSpec:
    # TODO: don't group by cell loc.
    cell_specs: Dict[CellLocation, List[CellExtractionSpec]]  # anchor -> specs
    table_specs: Dict[CellLocation,
                      List[TableExtractionSpec]]  # anchor -> specs

    def _deref(self,
               workbook: Workbook,
               make_dereferator: Callable[[Workbook, CellLocation], Dereferator]) -> 'ExcelProcessorSpec':
        cell_specs = {}
        for cl, ce_specs in self.cell_specs.items():
            dereferator = make_dereferator(workbook, cl)
            cell_specs[cl] = [ces.deref(dereferator) for ces in ce_specs]

        table_specs = {}
        for cl, te_specs in self.table_specs.items():
            dereferator = make_dereferator(workbook, cl)
            table_specs[cl] = [tes.deref(dereferator) for tes in te_specs]

        return ExcelProcessorSpec(
            cell_specs=cell_specs,
            table_specs=table_specs
        )

    def template_to_spec_deref(self, workbook: Workbook) -> 'ExcelProcessorSpec':
        """Transform raw spec to dereffed spec with template.
        Args:
            workbook(Workbook): Template workbook.
        Returns:
            Derefed ExcelProcessorSpec
        """
        return self._deref(workbook, Dereferator.template_to_spec)

    def spec_to_extractor_deref(self, workbook: Workbook) -> 'ExcelProcessorSpec':
        """Transform raw spec to derefed spec with to-be-extracted workbook.
        Args:
            workbook(Workbook): to-be-extracted workbook.
        Returns:
            Derefed ExcelProcessorSpec
        """
        return self._deref(workbook, Dereferator.spec_to_extractor)

    def n_total_spec(self) -> int:
        """total number of spec"""
        return self.n_table_spec() + self.n_cell_spec()

    def n_total_location(self) -> int:
        """total number of location with spec"""
        return len(set(self.cell_specs.keys()) | set(self.table_specs.keys()))

    def n_table_spec(self) -> int:
        """total number of table specs"""
        return util.flattened_len(self.table_specs.values())

    def n_cell_spec(self) -> int:
        """total number of cell specs"""
        return util.flattened_len(self.cell_specs.values())

    def n_cell_location(self) -> int:
        """total number of location with cell specs"""
        return len(self.cell_specs)

    def n_table_location(self) -> int:
        """total number of location with table spec"""
        return len(self.table_specs)

    def is_keys_unique(self) -> bool:
        """Check if keys are uniques
        Returns:
            bool. True if the keys are unique
        """
        it = chain(
            util.flatten(self.cell_specs.values()),
            util.flatten(self.table_specs.values()))
        return util.is_unique(
            spec.key for spec in it
        )

    @classmethod
    def from_workbook_template(cls, workbook: Workbook) -> 'ExcelProcessorSpec':
        """Create and deref spec from workbook template

        Args:
            workbook (Workbook): workbook

        Returns:
            ExcelProcessorSpec
        """
        from exco.exco_template import ExcoTemplate
        et = ExcoTemplate.from_workbook(workbook)
        raw_spec = et.to_raw_excel_processor_spec()
        return raw_spec.template_to_spec_deref(workbook)

    @classmethod
    def from_excel_template(cls, fname: str) -> 'ExcelProcessorSpec':
        """Create and deref spec from workbook template

        Args:
            fname (str): file name

        Returns:
            ExcelProcessorSpec
        """
        return cls.from_workbook_template(load_workbook(fname))
