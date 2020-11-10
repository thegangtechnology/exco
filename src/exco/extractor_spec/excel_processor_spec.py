from dataclasses import dataclass
from typing import Dict, List

from exco.cell_location import CellLocation
from exco import util
from exco.extractor_spec.cell_extraction_spec import CellExtractionSpec
from exco.extractor_spec.table_extraction_spec import TableExtractionSpec
from itertools import chain


@dataclass
class ExcelProcessorSpec:
    # TODO: don't group by cell loc.
    cell_specs: Dict[CellLocation, List[CellExtractionSpec]]  # anchor -> specs
    table_specs: Dict[CellLocation, List[TableExtractionSpec]]  # anchor -> specs

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
