from datetime import datetime
from typing import Optional, Tuple

from clients.openweather.openweather_client import OpenWeatherClient
from model.image_weather_info import ImageWeatherInfo


def get_weather_info(location: Tuple[float, float], date_time: datetime, open_weather_client: OpenWeatherClient) \
        -> Optional[ImageWeatherInfo]:
    """ Get weather information by given data in exif_info (location and data).
    :param date_time: datetime to get weather forecast for
    :param location: location to get weather forecast for
    :param open_weather_client: open weather client to get weather
    :return: image weather information
    """

    # Using api get weather for location and data in exif data
    weather_info = open_weather_client.get_history_weather(location, date_time)

    if weather_info is None:
        return None

    return ImageWeatherInfo(
        weather_id=weather_info.weather[0].id,
        temperature=weather_info.main.temp,
        wind_speed=weather_info.wind.speed,
        wind_direction=weather_info.wind.deg,
        clouds=weather_info.clouds.all,
        humidity=weather_info.main.humidity
    )


def read_weather_info():
    pass
