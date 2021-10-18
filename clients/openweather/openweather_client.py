from datetime import datetime, timedelta
from typing import Tuple

import requests
from dacite import from_dict

from clients.openweather.openweather_api import OpenWeatherResponse


class OpenWeatherClient:

    def __init__(self, key: str):
        self._key = key
        self._url = 'http://history.openweathermap.org/data/2.5/history/city'

    def get_weather(self, location: Tuple[float, float], date_time: datetime = None) -> OpenWeatherResponse:
        url = f'{self._url}?lat={location[0]}&lon={location[1]}' \
              f'&type=hour' \
              f'&appid={self._key}'

        if date_time is not None:
            if datetime.now().year - date_time.year > 1:
                date_time = datetime(year=date_time.year + (datetime.now().year - date_time.year - 1),
                                     month=date_time.month,
                                     day=date_time.day,
                                     hour=date_time.hour)

            url = f'{url}' \
                  f'&start={int((date_time - timedelta(hours=1)).timestamp())}' \
                  f'&end={int((date_time + timedelta(hours=1)).timestamp())}'

        response = requests.get(url).json()
        open_weather_response = from_dict(data_class=OpenWeatherResponse, data=response)
        return open_weather_response
