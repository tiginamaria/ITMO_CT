from dataclasses import dataclass

import pandas as pd

from database.model.columns import WeatherInfoColumnName


@dataclass
class ImageWeatherInfo:
    weather_id: int
    temperature: float
    wind_speed: float
    wind_direction: int
    clouds: int
    humidity: int

    @classmethod
    def from_row(cls, row: pd.Series) -> 'ImageWeatherInfo':
        return ImageWeatherInfo(
            weather_id=row[WeatherInfoColumnName.WEATHER_ID],
            temperature=row[WeatherInfoColumnName.TEMPERATURE],
            wind_speed=row[WeatherInfoColumnName.WIND_SPEED],
            wind_direction=row[WeatherInfoColumnName.WIND_DIRECTION],
            clouds=row[WeatherInfoColumnName.CLOUDS],
            humidity=row[WeatherInfoColumnName.HUMIDITY]
        )

    def to_json(self):
        return {
            WeatherInfoColumnName.WEATHER_ID: self.weather_id,
            WeatherInfoColumnName.TEMPERATURE: self.temperature,
            WeatherInfoColumnName.WIND_SPEED: self.wind_speed,
            WeatherInfoColumnName.WIND_DIRECTION: self.wind_direction,
            WeatherInfoColumnName.CLOUDS: self.clouds,
            WeatherInfoColumnName.HUMIDITY: self.humidity
        }
