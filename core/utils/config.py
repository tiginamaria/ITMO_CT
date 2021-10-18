import json
import os
from dataclasses import dataclass

from dacite import from_dict


@dataclass
class ClientConfig:
    yandex_geocoder_api_key: str
    yandex_weather_api_key: str
    open_weather_api_key: str


@dataclass
class DatabaseConfig:
    database_csv_file_path: str
    database_resources_path: str


@dataclass
class ResourceConfig:
    upload_dir: str


@dataclass
class Config:
    database: DatabaseConfig
    resource: ResourceConfig
    clients: ClientConfig


def load_config(config_dir: str) -> Config:
    with open(os.path.join(config_dir, 'config.json'), "r") as config_file:
        config_json = json.load(config_file)
        return from_dict(data_class=Config, data=config_json)
