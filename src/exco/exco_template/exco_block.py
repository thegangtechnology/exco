from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Iterable, Dict, Any

import yaml
from exco import setting
from exco.exception import TooManyBeginException, TooManyEndException, BadTemplateException, ExcoException, \
    TableKeyNotFound, ExpectEndException, YamlParseError
from exco.extractor_spec import CellExtractionSpec
from exco.extractor_spec.spec_source import SpecSource
from exco.setting import k_table_key
from yaml.scanner import ScannerError


@dataclass
class LineCollector:
    start_line: int
    raw: List[str] = field(default_factory=list)
    end_line: int = 0

    def __post_init__(self):
        self.end_line = self.start_line

    def append(self, i: int, line: str):
        self.end_line = i
        self.raw.append(line)


@dataclass
class ExcoBlock(SpecSource):
    start_line: int
    end_line: int
    raw: str

    def table_key(self) -> str:
        """

        Returns:
            str. table key for this block.
        """
        d = self.to_dict()
        try:
            return d[k_table_key]
        except LookupError as e:
            raise TableKeyNotFound() from e

    @property
    def key(self) -> str:
        """

        Returns:
            str. key for this block
        """
        return self.to_dict()[setting.k_key]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary.

        Returns:
            Dict[str, Any]
        """
        try:
            return yaml.load(self.raw, Loader=yaml.FullLoader)
        except ScannerError as e:
            raise YamlParseError(self.raw) from e

    def to_cell_extractor_task_spec(self) -> CellExtractionSpec:
        """To CellExtractionSpec

        Returns:
            CellExtractionSpecs
        """
        return CellExtractionSpec.from_dict(self.to_dict(), source=self)

    def describe(self) -> str:
        """

        Returns:
            String description of this block.
        """
        return self.raw

    @classmethod
    def from_line_collector(cls, line_collector: LineCollector) -> 'ExcoBlock':
        """Construct from line_collector.

        Args:
            line_collector (LineCollector):

        Returns:
            ExcoBlock
        """
        return ExcoBlock(
            start_line=line_collector.start_line,
            end_line=line_collector.end_line,
            raw='\n'.join(line_collector.raw)
        )

    @classmethod
    def simple(cls, raw: str, start_line: int = 0, end_line: int = 0) -> 'ExcoBlock':
        return ExcoBlock(
            raw=raw,
            start_line=start_line,
            end_line=end_line
        )


@dataclass
class ExcoBlockCollection:
    table_blocks: List[ExcoBlock]
    cell_blocks: List[ExcoBlock]
    column_blocks: List[ExcoBlock]

    def n_total_blocks(self) -> int:
        """

        Returns:
            total number of blocks.
        """
        return len(self.table_blocks) + len(self.cell_blocks) + len(self.column_blocks)

    @classmethod
    def from_string(cls, block: str):
        """Construct from comment string."""
        return ExcoBlockParser.parse(block.split('\n'))


class ExcoBlockParserState(Enum):
    OUTSIDE = auto()
    INSIDE_CELL = auto()
    INSIDE_TABLE = auto()
    INSIDE_COL = auto()

    def is_inside(self):
        return self != self.OUTSIDE

    def is_outside(self):
        return self == self.OUTSIDE


S = ExcoBlockParserState


class ExcoBlockParser:
    """
    FSM Parser for comment block.
    """

    @classmethod
    def enter_block(cls, cs: S, line: str, ns: S) -> S:
        """Enter block transition

        Args:
            cs (ExcoBlockParserState):
            line (str): this line
            ns (ExcoBlockParserState):

        Raises:
            TooManyBeginException. If try to enter when it's already enter.
        Returns:
            ExcoBlockParserState. Next State.
        """
        if cs.is_outside():
            return ns
        else:
            raise TooManyBeginException(f'Too many begin exception for {line}')

    @classmethod
    def compute_next_state(cls, current_state: S, line: str) -> S:
        """Compute the next state

        Args:
            current_state (ExcoBlockParserState):
            line (str):

        Raises:
            ExcoException on invalid transition

        Returns:
            ExcoBlockParserState. Next state.
        """
        cs = current_state
        if line == setting.start_table_marker:
            return cls.enter_block(cs, line, S.INSIDE_TABLE)
        elif line == setting.start_cell_marker:
            return cls.enter_block(cs, line, S.INSIDE_CELL)
        elif line == setting.start_col_marker:
            return cls.enter_block(cs, line, S.INSIDE_COL)
        elif line == setting.end_marker:
            if current_state.is_inside():
                return S.OUTSIDE
            else:
                raise TooManyEndException(f'Too many end markers.')
        else:
            return current_state

    @classmethod
    def parse(cls, lines: Iterable[str]) -> ExcoBlockCollection:
        """Parse the line iterable into ExcoBlockCollection

        Args:
            lines (Iterable[str]):

        Returns:
            ExcoBlockCollection
        """

        cs = S.OUTSIDE
        collectors: Dict[S, List[LineCollector]] = {
            S.INSIDE_TABLE: [],
            S.INSIDE_CELL: [],
            S.INSIDE_COL: []
        }
        current_collector = None
        try:
            for i, line in enumerate(lines, start=1):
                ns = cls.compute_next_state(cs, line)
                if cs.is_outside() and ns.is_inside():  # enter block
                    current_collector = LineCollector(i)
                elif cs.is_inside() and ns.is_inside():  # stay inside -> collect
                    current_collector.append(i, line)
                elif cs.is_inside() and ns.is_outside():  # exit block -> put in collectors
                    collectors[cs].append(current_collector)
                    current_collector = None
                cs = ns
            if cs.is_inside():
                raise ExpectEndException()

            return ExcoBlockCollection(
                table_blocks=[ExcoBlock.from_line_collector(lc) for lc in collectors[S.INSIDE_TABLE]],
                cell_blocks=[ExcoBlock.from_line_collector(lc) for lc in collectors[S.INSIDE_CELL]],
                column_blocks=[ExcoBlock.from_line_collector(lc) for lc in collectors[S.INSIDE_COL]]
            )
        except ExcoException as e:
            raise BadTemplateException(f'Bad template at Line {i}\n{lines}') from e
