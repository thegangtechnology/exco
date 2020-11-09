import logging
from dataclasses import dataclass
from typing import List

import yaml
from exco import exception as exc
from exco import setting
from exco.extractor_spec import CellExtractionSpec
from exco.extractor_spec.spec_source import SpecSource


@dataclass
class ExcoBlock(SpecSource):
    start_line: int
    end_line: int
    raw: str

    def to_extractor_task_spec(self) -> CellExtractionSpec:
        d = yaml.load(self.raw, Loader=yaml.FullLoader)
        return CellExtractionSpec.from_dict(d, source=self)

    def describe(self) -> str:
        return self.raw

    @classmethod
    def from_string(cls, comment: str,
                    start_marker=setting.start_marker,
                    end_marker=setting.end_marker) -> List['ExcoBlock']:
        in_marker = False
        current_str = ''
        start_line = None
        ret = []
        for i, line in enumerate(comment.splitlines(keepends=True), start=1):
            if line.strip() == start_marker:
                logging.debug(f'start {i}')
                if in_marker:
                    raise exc.TooManyBeginException(f"Expect end marker before another begin marker at line {i}.")
                in_marker = True
                start_line = i
            elif line.strip() == end_marker:
                logging.debug(f'end {i}')
                if not in_marker:
                    raise exc.TooManyEndException(f"Expect another begin marker at line {i}.")
                in_marker = False
                end_line = i
                ret.append(ExcoBlock(
                    start_line=start_line,
                    end_line=end_line,
                    raw=current_str
                ))
                current_str = ''
            elif in_marker:
                logging.debug(f'in_marker: {i} {line!r}')
                current_str += line
        if in_marker:
            raise exc.ExpectEndException("Expect End marker before the end.")
        return ret
