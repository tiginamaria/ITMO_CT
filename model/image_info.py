from dataclasses import dataclass

from database.model.columns import ImageInfoColumnName
from model.image_colors_info import ImageColorsInfo
from model.image_exif_info import ImageExifInfo
from model.image_weather_info import ImageWeatherInfo

import pandas as pd


@dataclass
class ImageInfo:
    path: str
    exif_info: ImageExifInfo
    weather_info: ImageWeatherInfo
    colors_info: ImageColorsInfo
    id: int = -1  # default value for not indexed images

    def to_json(self):
        return {
            ImageInfoColumnName.ID: self.id,
            ImageInfoColumnName.PATH: self.path,
            **self.exif_info.to_json(),
            **self.weather_info.to_json(),
            **self.colors_info.to_json()
        }

    @classmethod
    def from_row(cls, row: pd.Series) -> 'ImageInfo':
        return ImageInfo(
            id=row[ImageInfoColumnName.ID],
            path=row[ImageInfoColumnName.PATH],
            exif_info=ImageExifInfo.from_row(row),
            weather_info=ImageWeatherInfo.from_row(row),
            colors_info=ImageColorsInfo.from_row(row)
        )
