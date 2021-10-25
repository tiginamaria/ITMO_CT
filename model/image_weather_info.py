from dataclasses import dataclass
from typing import Optional


@dataclass
class ImageWeatherInfo:
    clouds: int
    weather_id: Optional[int] = None
    temperature: Optional[float] = None
    wind_speed: Optional[float] = None
    wind_direction: Optional[int] = None
    humidity: Optional[int] = None

    @classmethod
    def from_row(cls, row) -> 'ImageWeatherInfo':
        return ImageWeatherInfo(
            clouds=row[0]
        )
