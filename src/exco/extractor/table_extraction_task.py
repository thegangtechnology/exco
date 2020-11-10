from dataclasses import dataclass, field
from typing import Dict, List, Any

from exco import CellLocation
from exco.exception import TooManyRowRead
from exco.extractor import Locator
from exco.extractor.cell_extraction_task import CellExtractionTaskResult, CellExtractionTask
from exco.extractor.locator.locating_result import LocatingResult
from exco.extractor.table_end_conditions.table_end_condition import TableEndCondition
from exco.extractor.table_end_conditions.table_end_condition_param import TableEndConditionParam
from exco.extractor.table_end_conditions.table_end_condition_result import TableEndConditionResult
from exco.extractor_spec.table_extraction_spec import TableItemDirection
from openpyxl import Workbook
from exco import setting as st


@dataclass
class EndConditionCollectionResult:
    end_condition_results: List[TableEndConditionResult]

    def should_terminate_exclusively(self) -> bool:
        """

        Returns:
            bool. should terminate without parsing this row
        """
        return any(ecr.should_terminate and ecr.is_exclusive for ecr in self.end_condition_results)

    def should_terminate_inclusively(self) -> bool:
        """

        Returns:
            bool. should terminate after parsing this row
        """
        return any(ecr.should_terminate and ecr.is_inclusive for ecr in self.end_condition_results)


@dataclass
class EndConditionCollection:
    end_conditions: List[TableEndCondition]

    def test(self, param: TableEndConditionParam) -> EndConditionCollectionResult:
        return EndConditionCollectionResult(
            end_condition_results=[ec.test(param) for ec in self.end_conditions]
        )


@dataclass
class RowExtractionTaskResult:
    cell_results: Dict[str, CellExtractionTaskResult]

    def to_dict(self) -> Dict[str, Any]:
        return {k: v.get_value(None) for k, v in self.cell_results.items()}


@dataclass
class TableExtractionTaskResult:
    key: str
    locating_result: LocatingResult
    row_results: List[RowExtractionTaskResult] = field(default_factory=list)
    # should I only keep the last one??
    end_condition_results: List[EndConditionCollectionResult] = field(default_factory=list)

    @classmethod
    def fail_locating_result(cls, locating_result: LocatingResult) -> 'TableExtractionTaskResult':
        return TableExtractionTaskResult(locating_result=locating_result)

    def get_value(self, default: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [res.to_dict() for res in self.row_results]


@dataclass
class TableExtractionTask:
    key: str
    locator: Locator
    columns: Dict[int, CellExtractionTask]  # offset -> APVSpec
    end_condition: EndConditionCollection  # there is inclusive and exclusive
    item_direction: TableItemDirection = TableItemDirection.DOWNWARD

    def shift_item_direction(self, cl: CellLocation, offset: int = 1) -> CellLocation:
        if self.item_direction == TableItemDirection.DOWNWARD:
            return cl.shift_row(offset)
        else:
            return cl.shift_col(offset)

    def shift_column_direction(self, cl: CellLocation, offset: int) -> CellLocation:
        if self.item_direction == TableItemDirection.DOWNWARD:
            return cl.shift_col(offset)
        else:
            return cl.shift_row(offset)

    def build_row_cell_locations(self, key_cell: CellLocation) -> Dict[str, CellLocation]:
        return {cet.key: self.shift_column_direction(key_cell, offset) for offset, cet in self.columns.items()}

    def process(self, anchor_cell_location: CellLocation, workbook: Workbook) -> TableExtractionTaskResult:
        locating_result = self.locator.locate(anchor_cell_location, workbook)
        if not locating_result.is_ok:
            return TableExtractionTaskResult.fail_locating_result(locating_result)

        irow = 0
        should_terminate = False
        key_cell = anchor_cell_location
        row_results = []
        end_condition_results = []
        while not should_terminate:
            irow += 1
            if irow >= st.table_infinite_loop_guard:
                raise TooManyRowRead(f'setting.table_infinite_loop_guard ({st.table_infinite_loop_guard}) reached')
            cell_locations = self.build_row_cell_locations(key_cell)
            cfps = {k: cl.get_cell_full_path(workbook) for k, cl in cell_locations.items()}

            # Test end condition
            ec_param = TableEndConditionParam(row_count=irow, cfps=cfps)
            ec_results = self.end_condition.test(ec_param)
            end_condition_results.append(ec_results)
            if ec_results.should_terminate_exclusively():
                break

            # parse
            cell_results = []
            for offset, cet in self.columns.items():
                cell_cl = self.shift_column_direction(key_cell, offset)
                cell_results.append(cet.process(cell_cl, workbook))

            if ec_results.should_terminate_inclusively():
                break

            # shift
            key_cell = self.shift_item_direction(key_cell)

        return TableExtractionTaskResult(
            key=self.key,
            locating_result=locating_result,
            row_results=row_results,
            end_condition_results=end_condition_results
        )
