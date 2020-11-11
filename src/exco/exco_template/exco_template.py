import itertools
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List

import openpyxl as opx
from exco import util
from exco.cell_location import CellLocation
from exco.exception import ExcoException, BadTemplateException, CommentWithNoExcoBlockWarning, TableKeyNotFound, \
    TableHasNoColumn, MissingTableBlock
from exco.exco_template.exco_block import ExcoBlock, ExcoBlockCollection
from exco.extractor_spec.cell_extraction_spec import CellExtractionSpec
from exco.extractor_spec.excel_processor_spec import ExcelProcessorSpec
from exco.extractor_spec.spec_source import SpecSource
from exco.extractor_spec.table_extraction_spec import TableExtractionSpec, ColumnSpecDict
from openpyxl.cell.read_only import EmptyCell
import warnings


@dataclass
class ExcoBlockWithLocation(SpecSource):
    cell_location: CellLocation
    exco_block: ExcoBlock

    @property
    def key(self) -> str:
        """

        Returns:
            Block's key
        """
        return self.exco_block.key

    def describe(self) -> str:
        """

        Returns:
            Block description.
        """
        return self.cell_location.sheet_name + '\n' + self.exco_block.raw

    @classmethod
    def simple(cls, raw: str,
               sheet: str = 'SHEET1',
               coord: str = 'A1',
               start_line: int = 1,
               end_line: int = 1):
        return ExcoBlockWithLocation(
            cell_location=CellLocation(sheet, coord),
            exco_block=ExcoBlock(
                start_line=start_line,
                end_line=end_line,
                raw=raw
            )
        )


@dataclass
class ExcoTemplate:
    table_blocks: List[ExcoBlockWithLocation]
    column_blocks: List[ExcoBlockWithLocation]
    cell_blocks: List[ExcoBlockWithLocation]

    @classmethod
    def empty(cls) -> 'ExcoTemplate':
        """Create Empty Template

        Returns:
            ExcoTemplate
        """
        return ExcoTemplate(table_blocks=[], column_blocks=[], cell_blocks=[])

    def add_to_block_collections(self, cell_location: CellLocation, block_collection: ExcoBlockCollection) -> None:
        """Add block collection as if anchor cell is at cell_location.

        Args:
            cell_location (CellLocation):
            block_collection (ExcoBlockCollection):

        Returns:
            None.
        """

        for tb in block_collection.table_blocks:
            self.table_blocks.append(ExcoBlockWithLocation(cell_location, tb))
        for cell_block in block_collection.cell_blocks:
            self.cell_blocks.append(ExcoBlockWithLocation(cell_location, cell_block))
        for col_block in block_collection.column_blocks:
            self.column_blocks.append(ExcoBlockWithLocation(cell_location, col_block))

    def cell_locations(self) -> List[CellLocation]:
        """

        Returns:
            List of unique cell locations
        """
        return util.unique(x.cell_location for x in itertools.chain(
            self.table_blocks,
            self.column_blocks,
            self.cell_blocks
        ))

    def n_cell(self) -> int:
        """

        Returns:
            Total number of cells with comments. Some comment may have no exco block.
        """
        return len(self.cell_locations())

    def n_exco_blocks(self) -> int:
        """

        Returns:
            Total number of ExcoBlocks
        """
        return len(self.table_blocks) + len(self.column_blocks) + len(self.cell_blocks)

    @classmethod
    def from_workbook(cls, workbook: opx.Workbook) -> 'ExcoTemplate':
        """Construct from Excel workbook

        Args:
            workbook (workbook):

        Returns:
            ExcoTemplate
        """
        wb = workbook
        ret = ExcoTemplate.empty()
        for cfp in util.iterate_cells_in_workbook(wb):
            if not isinstance(cfp.cell, EmptyCell) and cfp.cell.comment is not None:
                cell_loc = cfp.to_cell_location()
                try:
                    ebc = ExcoBlockCollection.from_string(cfp.cell.comment.text)
                    if ebc.n_total_blocks() == 0:
                        warnings.warn(f"{cell_loc.short_name} has comment but no exco block.",
                                      CommentWithNoExcoBlockWarning)
                    ret.add_to_block_collections(cell_loc, ebc)
                except ExcoException as e:  # throw error with cell info
                    raise BadTemplateException(  # Todo: maybe be all these should be warning
                        f'Bad Template at sheet: {cell_loc.sheet_name}, cell: {cell_loc.coordinate}') from e
        return ret

    @classmethod
    def from_excel(cls, fname: str) -> 'ExcoTemplate':
        """Construct from excel file.

        Args:
            fname (str): file name.

        Returns:
            ExcoTemplate
        """
        return cls.from_workbook(workbook=opx.load_workbook(fname))

    def column_block_dict_by_table_key(self) -> Dict[str, List[ExcoBlockWithLocation]]:
        """ Compute column block dicationary grouped by table key

        Returns:
            Dict[str, List[ExcoBlockWithLocation]]. TableKey -> [Column's ExcoBlock]
        """

        def get_table_key(block: ExcoBlockWithLocation):
            try:
                return block.exco_block.table_key()
            except ExcoException as e:
                raise TableKeyNotFound(f'{block.cell_location.short_name}') from e

        return util.group_by(get_table_key, self.column_blocks)

    def build_table_specs(self) -> Dict[CellLocation, List[TableExtractionSpec]]:
        """build table spec

        Returns:
            Dict[CellLocation, List[TableExtractionSpec]]. Anchor -> List[TableExtractionSpec]
        """
        group_columns = self.column_block_dict_by_table_key()
        used_keys = []
        ret: Dict[CellLocation, List[TableExtractionSpec]] = defaultdict(list)
        for tb in self.table_blocks:
            table_key = tb.key
            table_loc = tb.cell_location
            used_keys.append(table_key)
            try:
                column_blocks = group_columns[table_key]
            except LookupError as e:
                raise TableHasNoColumn(table_key) from e
            # TODO: Support other orientation by allowing tuple
            columns_dicts = []
            for cb in column_blocks:
                offset = tb.cell_location.offset_to(cb.cell_location)[1]
                columns_dicts.append(ColumnSpecDict(
                    offset=offset, dict=cb.exco_block.to_dict(), source=cb
                ))
            table_spec = TableExtractionSpec.from_table_and_column_dict(
                d=tb.exco_block.to_dict(),
                source=tb,
                column_dicts=columns_dicts
            )
            ret[table_loc].append(table_spec)

        if len(group_columns) != len(used_keys):
            missing_key = [gc for gc in group_columns.keys() if gc not in used_keys]
            raise MissingTableBlock(f"{missing_key} has no matching table block.")
        return dict(ret)

    def build_cell_specs(self) -> Dict[CellLocation, List[CellExtractionSpec]]:
        """build cell specs

        Returns:
             Dict[CellLocation, List[CellExtractionSpec]]. Anchor to CellExtractionSpec.
        """

        ret: Dict[CellLocation, List[CellExtractionSpec]] = defaultdict(list)

        for cb in self.cell_blocks:
            cl = cb.cell_location
            try:
                ret[cl].append(CellExtractionSpec.from_dict(cb.exco_block.to_dict(), cb))
            except ExcoException as e:
                raise BadTemplateException(cl.short_name) from e
        return dict(ret)

    def to_excel_extractor_spec(self) -> ExcelProcessorSpec:
        """compute excel extractor spec

        Returns:
            ExcelProcessorSpec
        """
        return ExcelProcessorSpec(
            cell_specs=self.build_cell_specs(),
            table_specs=self.build_table_specs())
