from datetime import datetime, timedelta
from typing import Tuple, Optional

import logging
import requests
from dacite import from_dict

from clients.openweather.openweather_api import OpenWeatherResponse, WeatherFullInfo


class OpenWeatherClient:
    """ Client for data exchange using openweather api. """

    def __init__(self, key: str):
        self._key = key
        self._url = 'http://history.openweathermap.org/data/2.5/history/city'

    def get_history_weather(self, location: Tuple[float, float], date_time: datetime) -> Optional[WeatherFullInfo]:
        """ Method get weather forecast for given location and datatime from openweather service.
        :param location: where to get weather
        :param date_time: when to get weather
        :return: open weather response
        """

        url = f'{self._url}?lat={location[0]}&lon={location[1]}&type=hour&appid={self._key}'

        # Openweather student pack api provides only 1 year back forecasts, so id given datatime is out of this range,
        # request is build for the same day but less then 1 year back
        if datetime.now().year - date_time.year > 1:
            logging.warning(f"Given datetime {date_time} is more then 1 year back")
            date_time = datetime(year=date_time.year + (datetime.now().year - date_time.year - 1),
                                 month=date_time.month,
                                 day=date_time.day,
                                 hour=date_time.hour)
            logging.warning(f"Building request for datetime {date_time}")

        url = f'{url}' \
              f'&start={int((date_time - timedelta(hours=1)).timestamp())}' \
              f'&end={int((date_time + timedelta(hours=1)).timestamp())}'

        # Sending request to openweather server
        response = requests.get(url).json()

        # Parsing openweather response
        open_weather_response = from_dict(data_class=OpenWeatherResponse, data=response)

        # If answer is empty return None
        if open_weather_response.list is None or len(open_weather_response.list) == 0:
            return None
        return open_weather_response.list[0]
