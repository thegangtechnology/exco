from dataclasses import dataclass
from typing import Dict, List, Callable

from exco.cell_location import CellLocation
from exco import util
from exco.dereferator import Dereferator
from exco.extractor_spec.cell_extraction_spec import CellExtractionSpec
from exco.extractor_spec.table_extraction_spec import TableExtractionSpec
from itertools import chain

from openpyxl import Workbook


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
        return self._deref(workbook, Dereferator.template_to_spec)

    def spec_to_extractor_deref(self, workbook: Workbook) -> 'ExcelProcessorSpec':
        return self._deref(workbook, Dereferator.spec_to_extractor)

    def n_total_spec(self) -> int:
        return self.n_table_spec() + self.n_cell_spec()

    def n_total_location(self) -> int:
        return len(set(self.cell_specs.keys()) | set(self.table_specs.keys()))

    def n_table_spec(self) -> int:
        return util.flattened_len(self.table_specs.values())

    def n_cell_spec(self) -> int:
        return util.flattened_len(self.cell_specs.values())

    def n_cell_location(self) -> int:
        return len(self.cell_specs)

    def n_table_location(self) -> int:
        return len(self.table_specs)

    def is_keys_unique(self) -> bool:
        it = chain(
            util.flatten(self.cell_specs.values()),
            util.flatten(self.table_specs.values()))
        return util.is_unique(
            spec.key for spec in it
        )
