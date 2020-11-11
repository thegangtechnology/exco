from dataclasses import dataclass, field
from typing import Dict, List, Any

from exco import CellLocation
from exco.exception import TooManyRowRead, NoEndConditonError
from exco.extractor.locator.locator import Locator
from exco.extractor.cell_extraction_task import CellExtractionTaskResult, CellExtractionTask
from exco.extractor.locator.locating_result import LocatingResult
from exco.extractor.table_end_conditions.built_in.all_blank_table_end_condition import AllBlankTableEndCondition
from exco.extractor.table_end_conditions.table_end_condition import TableEndCondition
from exco.extractor.table_end_conditions.table_end_condition_factory import TableEndConditionFactory
from exco.extractor.table_end_conditions.table_end_condition_param import TableEndConditionParam
from exco.extractor.table_end_conditions.table_end_condition_result import TableEndConditionResult
from exco.extractor_spec.table_extraction_spec import TableItemDirection, TableEndConditionSpec
from openpyxl import Workbook
from exco import setting as st


@dataclass
class EndConditionCollectionResult:
    end_condition_results: List[TableEndConditionResult]

    @property
    def is_ok(self) -> bool:
        """

        Returns:
            bool. True if the result is ok.
        """
        return all(x.is_ok for x in self.end_condition_results)

    def should_terminate_exclusively(self) -> bool:
        """

        Returns:
            bool. should terminate WITHOUT parsing this row
        """
        return any(ecr.should_terminate and ecr.is_exclusive for ecr in self.end_condition_results)

    def should_terminate_inclusively(self) -> bool:
        """

        Returns:
            bool. should terminate AFTER parsing this row
        """
        return any(ecr.should_terminate and ecr.is_inclusive for ecr in self.end_condition_results)


@dataclass
class EndConditionCollection:
    """Collection of End Condtition.
    When it's tested all the endcondition are applied sequentially.
    """
    end_conditions: List[TableEndCondition]

    def test(self, param: TableEndConditionParam) -> EndConditionCollectionResult:
        return EndConditionCollectionResult(
            end_condition_results=[ec.test(param) for ec in self.end_conditions]
        )

    @classmethod
    def from_spec(cls,
                  specs: List[TableEndConditionSpec],
                  factory: TableEndConditionFactory) -> 'EndConditionCollection':
        if not specs:
            raise NoEndConditonError()
        ecs = [factory.create_from_spec(spec) for spec in specs]

        return EndConditionCollection(end_conditions=ecs)

    @classmethod
    def default(cls) -> 'EndConditionCollection':
        return EndConditionCollection([AllBlankTableEndCondition()])


@dataclass
class RowExtractionTaskResult:
    """Extraction Result for a Row"""
    cell_results: Dict[str, CellExtractionTaskResult]

    @property
    def is_ok(self) -> bool:
        return all(x.is_ok for x in self.cell_results.values())

    def to_dict(self) -> Dict[str, Any]:
        return {k: v.get_value(None) for k, v in self.cell_results.items()}


@dataclass
class TableExtractionTaskResult:
    """Extraction Result for a Table"""
    key: str
    locating_result: LocatingResult
    row_results: List[RowExtractionTaskResult] = field(default_factory=list)
    end_condition_results: List[EndConditionCollectionResult] = field(default_factory=list)

    @property
    def is_ok(self):
        return self.locating_result.is_ok and \
               all(rr.is_ok for rr in self.row_results) and \
               all(ec.is_ok for ec in self.end_condition_results)

    @classmethod
    def fail_locating_result(cls, key: str, locating_result: LocatingResult) -> 'TableExtractionTaskResult':
        """TableExtractionTaskResult when it fails locating the cell

        Args:
            locating_result (LocatingResult):

        Returns:
            TableExtractionTaskResult
        """
        return TableExtractionTaskResult(key=key, locating_result=locating_result)

    def get_value(self) -> List[Dict[str, Any]]:
        """
        Returns:
            Python Equivalent Value
        """
        return [res.to_dict() for res in self.row_results]


@dataclass
class TableExtractionTask:
    key: str
    locator: Locator
    columns: Dict[int, CellExtractionTask]  # offset -> APVSpec
    end_condition: EndConditionCollection  # there is inclusive and exclusive
    item_direction: TableItemDirection = TableItemDirection.DOWNWARD

    def shift_item_direction(self, cl: CellLocation, offset: int = 1) -> CellLocation:
        """Shift cell location in the item direction.

        Args:
            cl (CellLocation):
            offset (int):

        Returns:
            CellLocation
        """
        if self.item_direction == TableItemDirection.DOWNWARD:
            return cl.shift_row(offset)
        else:
            return cl.shift_col(offset)

    def shift_column_direction(self, cl: CellLocation, offset: int) -> CellLocation:
        """Shift cell location in the column direction.

        Args:
            cl ():
            offset ():

        Returns:

        """
        if self.item_direction == TableItemDirection.DOWNWARD:
            return cl.shift_col(offset)
        else:
            return cl.shift_row(offset)

    def _build_row_cell_locations(self, key_cell: CellLocation) -> Dict[str, CellLocation]:
        """Build a dictionary from column key to each columns' CellLocation.
        The offset is applied and the key is change to column key

        Args:
            key_cell (CellLocation):

        Returns:
            Dict[str, CellLocation]. column key -> CellLocation
        """
        return {cet.key: self.shift_column_direction(key_cell, offset) for offset, cet in self.columns.items()}

    def process(self, anchor_cell_location: CellLocation, workbook: Workbook) -> TableExtractionTaskResult:
        """ Extract table from work book as if the anchor location is at anchor_cell_location

        Args:
            anchor_cell_location (CellLocation):
            workbook (Workbook):

        Returns:

        """
        locating_result = self.locator.locate(anchor_cell_location, workbook)
        if not locating_result.is_ok:
            return TableExtractionTaskResult.fail_locating_result(key=self.key, locating_result=locating_result)

        irow = 0
        should_terminate = False
        key_cell = anchor_cell_location
        row_results = []
        end_condition_results = []
        while not should_terminate:
            irow += 1
            if irow >= st.table_infinite_loop_guard:
                raise TooManyRowRead(f'setting.table_infinite_loop_guard ({st.table_infinite_loop_guard}) reached')
            cell_locations = self._build_row_cell_locations(key_cell)
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
            row_results.append(RowExtractionTaskResult(
                {cr.key: cr for cr in cell_results}
            ))
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
