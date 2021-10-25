from dataclasses import dataclass
from typing import Optional

from model.image_colors_info import ImageColorsInfo
from model.image_exif_info import ImageExifInfo
from model.image_weather_info import ImageWeatherInfo


@dataclass
class ImageInfo:
    id: int
    name: str
    exif_info: ImageExifInfo
    weather_info: ImageWeatherInfo
    colors_info: ImageColorsInfo
    image_path: Optional[str] = None
    palette_path: Optional[str] = None
    clusters_path: Optional[str] = None
