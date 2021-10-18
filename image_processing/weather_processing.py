from clients.openweather.openweather_client import OpenWeatherClient
from model.image_exif_info import ImageExifInfo
from model.image_weather_info import ImageWeatherInfo


def get_weather_data(exif_info: ImageExifInfo) -> ImageWeatherInfo:
    """ Get weather information by given data in exif_info (location and data).
    :param exif_info: image exif information
    :return: image weather information
    """

    # Create client object
    open_weather_client = OpenWeatherClient('5fd3acb9e271365266e92fce70c407d3')

    # Using api get weather for location and data in exif data
    open_weather_response = open_weather_client.get_weather((exif_info.gps_info.latitude, exif_info.gps_info.longitude),
                                                            exif_info.data_time.date_time)
    info = open_weather_response.list[0]
    return ImageWeatherInfo(
        weather_id=info.weather[0].id,
        temperature=info.main.temp,
        wind_speed=info.wind.speed,
        wind_direction=info.wind.deg,
        clouds=info.clouds.all,
        humidity=info.main.humidity
    )
