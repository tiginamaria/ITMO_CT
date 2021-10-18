from typing import Tuple, Optional

import requests
from dacite import from_dict

from clients.utils import preprocess_json, camel_to_underscore, str_to_number
from clients.yandex_geocoder.yandex_geocoder_api import YandexGeocoderResponse


class YandexGeocoderClient:

    def __init__(self, key: str):
        self._key = key
        self._url = 'https://geocode-maps.yandex.ru/1.x/'

    def get_location_by_address(self, address: str) -> Optional[Tuple[float, float]]:
        url = f'{self._url}?apikey={self._key}&geocode=${address}&format=json'
        response = requests.get(url).json()['response']
        preprocessed_response = preprocess_json(response, camel_to_underscore, str_to_number)
        geocoder_response = from_dict(data_class=YandexGeocoderResponse, data=preprocessed_response)
        if geocoder_response.geo_object_collection.meta_data_property.geocoder_response_meta_data.found == 0:
            return None
        else:
            return geocoder_response.geo_object_collection.feature_member[0].geo_object.point.to_lat_lon()
