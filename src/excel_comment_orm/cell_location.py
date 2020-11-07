from dataclasses import dataclass

from openpyxl.utils import coordinate_to_tuple


@dataclass(frozen=True)
class CellLocation:
    sheet_name: str
    coordinate: str

    def __hash__(self):
        return hash((self.sheet_name, self.coordinate))

    @property
    def short_name(self) -> str:
        return f"{self.sheet_name}!{self.coordinate}"

    @property
    def row(self) -> int:
        r, _ = coordinate_to_tuple(self.coordinate)
        return r

    @property
    def col(self) -> int:
        _, c = coordinate_to_tuple(self.coordinate)
        return c
