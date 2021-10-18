from enum import Enum


class WeatherInfoColumnName(str, Enum):
    WEATHER_ID = 'weather_id'
    TEMPERATURE = 'temperature'
    WIND_SPEED = 'wind_speed'
    WIND_DIRECTION = 'wind_direction'
    CLOUDS = 'clouds'
    HUMIDITY = 'humidity'


class ColorsInfoColumnName(str, Enum):
    COLORS = 'colors'


class ExifInfoColumnName(str, Enum):
    DATETIME = 'datetime'
    SEASON = 'season'
    LATITUDE = 'latitude'
    LONGITUDE = 'longitude'


class ImageInfoColumnName(str, Enum):
    ID = 'id'
    NAME = 'name'


COLUMNS_NAMES = [ImageInfoColumnName.ID,
                 ImageInfoColumnName.NAME,
                 ExifInfoColumnName.DATETIME,
                 ExifInfoColumnName.SEASON,
                 ExifInfoColumnName.LATITUDE,
                 ExifInfoColumnName.LONGITUDE,
                 WeatherInfoColumnName.WEATHER_ID,
                 WeatherInfoColumnName.TEMPERATURE,
                 WeatherInfoColumnName.WIND_SPEED,
                 WeatherInfoColumnName.WIND_DIRECTION,
                 WeatherInfoColumnName.HUMIDITY,
                 ColorsInfoColumnName.COLORS]
