from typing import Tuple, Optional

import requests
from dacite import from_dict

from clients.utils import preprocess_json, camel_to_underscore, str_to_number
from clients.yandex_geocoder.yandex_geocoder_api import YandexGeocoderResponse


class YandexGeocoderClient:
    """ Client for data exchange using yandex geocoder api. """

    def __init__(self, key: str):
        self._key = key
        self._url = 'https://geocode-maps.yandex.ru/1.x/'

    def get_location_by_address(self, address: str) -> Optional[Tuple[float, float]]:
        """ Get get location (lat, lon) for given address
        :param address: address to egt location for
        :return: location as a tuple (lat, lon)
        """
        url = f'{self._url}?apikey={self._key}&geocode=${address}&format=json'

        # Send request from geocoder service
        response = requests.get(url).json()['response']

        # Preprocess received json to have keys in underscore pattern and parse int/float values from string
        preprocessed_response = preprocess_json(response, camel_to_underscore, str_to_number)

        # Parse response
        geocoder_response = from_dict(data_class=YandexGeocoderResponse, data=preprocessed_response)

        # If answer is not presented return None
        if geocoder_response.geo_object_collection.meta_data_property.geocoder_response_meta_data.found == 0:
            return None
        else:
            return geocoder_response.geo_object_collection.feature_member[0].geo_object.point.to_lat_lon()
