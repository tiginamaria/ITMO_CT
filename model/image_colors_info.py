from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class ImageColorInfo:
    r: float
    g: float
    b: float
    percent: int

    @classmethod
    def from_row(cls, row: Tuple) -> 'ImageColorInfo':
        return ImageColorInfo(
            r=row[0],
            g=row[1],
            b=row[2],
            percent=row[3]
        )


@dataclass
class ImageColorsInfo:
    colors: List[ImageColorInfo]
