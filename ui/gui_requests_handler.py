import sys
from datetime import datetime
from pathlib import Path

from typing import List, Tuple

from clients.openweather.openweather_client import OpenWeatherClient
from clients.yandex_geocoder.yandex_geocoder_client import YandexGeocoderClient
from ui.finder_location_gui import UserLocation
from ui.upload_photo_gui import PhotoSelector
from utils.config import load_config

PROJECT_DIR = Path(__file__).parents[1]
RESOURCES_DIR = PROJECT_DIR / 'resources'


def select_photos_to_upload() -> List[str]:
    photos_selector = PhotoSelector(sys.argv)
    photos_selector.setQuitOnLastWindowClosed(True)
    selected_photos_path = photos_selector.run_ui().copy()
    del photos_selector
    return selected_photos_path


def get_current_location() -> Tuple[float, float]:
    user_location_gui = UserLocation()
    user_location_list = user_location_gui.run_gui()
    del user_location_gui

    config = load_config(RESOURCES_DIR)
    # Checking type of response
    if len(user_location_list) == 1:
        geocoder_client = YandexGeocoderClient(config.clients.yandex_geocoder_api_key)
        lat, lon = geocoder_client.get_location_by_address(user_location_list[0])
        user_location = (lat, lon)
    else:
        user_location = (float(user_location_list[0]), float(user_location_list[0]))

    return user_location


def get_current_date_time() -> datetime:
    return datetime.now()


def get_current_weather(location: Tuple[float, float]) -> int:
    config = load_config(RESOURCES_DIR)
    weather_client = OpenWeatherClient(config.clients.open_weather_api_key)
    current_weather = weather_client.get_current_weather(location).clouds.all
    return current_weather
