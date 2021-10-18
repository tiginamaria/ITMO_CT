from typing import Optional

from clients.openweather.openweather_client import OpenWeatherClient
from model.image_exif_info import ImageExifInfo
from model.image_weather_info import ImageWeatherInfo


def get_weather_data(exif_info: ImageExifInfo, api_key: str) -> Optional[ImageWeatherInfo]:
    """ Get weather information by given data in exif_info (location and data).
    :param api_key: api_key for open_weather
    :param exif_info: image exif information
    :return: image weather information
    """

    # Create client object
    open_weather_client = OpenWeatherClient(api_key)

    # Using api get weather for location and data in exif data
    weather_info = open_weather_client.get_history_weather(
        (exif_info.gps_info.latitude, exif_info.gps_info.longitude),
        exif_info.data_time.date_time)

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
