import logging
from dataclasses import dataclass, field
from enum import Enum, auto
from functools import lru_cache
from typing import List, Iterable, Dict, Optional

import yaml
from exco import exception as exc
from exco import setting
from exco.exception import TooManyBeginException, TooManyEndException, BadTemplateException, ExcoException, \
    TableKeyNotFound, ExpectEndException
from exco.extractor_spec import CellExtractionSpec
from exco.extractor_spec.spec_source import SpecSource
from exco.extractor_spec.table_extraction_spec import TableExtractionSpec
from exco.setting import k_table_key


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

    def table_key(self):
        d = self.to_dict()
        try:
            return d[k_table_key]
        except LookupError as e:
            raise TableKeyNotFound() from e

    @property
    def key(self):
        return self.to_dict()[setting.k_key]

    def to_dict(self):
        return yaml.load(self.raw, Loader=yaml.FullLoader)

    def to_extractor_task_spec(self) -> CellExtractionSpec:
        return CellExtractionSpec.from_dict(self.to_dict(), source=self)

    def describe(self) -> str:
        return self.raw

    @classmethod
    def from_line_collector(cls, line_collector: LineCollector) -> 'ExcoBlock':
        return ExcoBlock(
            start_line=line_collector.start_line,
            end_line=line_collector.end_line,
            raw='\n'.join(line_collector.raw)
        )


@dataclass
class ExcoBlockCollection:
    table_blocks: List[ExcoBlock]
    cell_blocks: List[ExcoBlock]
    column_blocks: List[ExcoBlock]

    def n_total_blocks(self) -> int:
        return len(self.table_blocks) + len(self.cell_blocks) + len(self.column_blocks)

    @classmethod
    def from_string(cls, block: str):
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
    @classmethod
    def enter_block(cls, cs: S, line: str, ns: S):
        if cs.is_outside():
            return ns
        else:
            raise TooManyBeginException(f'Too many begin exception for {line}')

    @classmethod
    def compute_next_state(cls, current_state: S, line: str) -> S:
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

    # @classmethod
    # def from_string(cls, comment: str,
    #                 start_marker=setting.start_marker,
    #                 end_marker=setting.end_marker) -> List['ExcoBlock']:
    #     in_marker = False
    #     current_str = ''
    #     start_line = None
    #     ret = []
    #     for i, line in enumerate(comment.splitlines(keepends=True), start=1):
    #         if line.strip() == start_marker:
    #             logging.debug(f'start {i}')
    #             if in_marker:
    #                 raise exc.TooManyBeginException(f"Expect end marker before another begin marker at line {i}.")
    #             in_marker = True
    #             start_line = i
    #         elif line.strip() == end_marker:
    #             logging.debug(f'end {i}')
    #             if not in_marker:
    #                 raise exc.TooManyEndException(f"Expect another begin marker at line {i}.")
    #             in_marker = False
    #             end_line = i
    #             ret.append(ExcoBlock(
    #                 start_line=start_line,
    #                 end_line=end_line,
    #                 raw=current_str
    #             ))
    #             current_str = ''
    #         elif in_marker:
    #             logging.debug(f'in_marker: {i} {line!r}')
    #             current_str += line
    #     if in_marker:
    #         raise exc.ExpectEndException("Expect End marker before the end.")
    #     return ret
