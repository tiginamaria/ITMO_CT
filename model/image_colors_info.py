from dataclasses import dataclass
from typing import List

import pandas as pd
from dacite import from_dict

from database.model.columns import ColorsInfoColumnName


@dataclass
class ImageColorInfo:
    r: float
    g: float
    b: float
    hex: str
    percent: float

    def to_json(self):
        return {
            'r': self.r,
            'g': self.g,
            'b': self.b,
            'hex': self.hex,
            'percent': self.percent
        }


@dataclass
class ImageColorsInfo:
    colors: List[ImageColorInfo]

    @classmethod
    def from_row(cls, row: pd.Series) -> 'ImageColorsInfo':
        info_json = row[ColorsInfoColumnName.COLORS]
        image_color_info = from_dict(data_class=ImageColorsInfo, data=info_json)
        return image_color_info

    def to_json(self):
        return {
            ColorsInfoColumnName.COLORS: [color.to_json() for color in self.colors]
        }
