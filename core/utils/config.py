import json
import os
from dataclasses import dataclass

from dacite import from_dict


@dataclass
class ClientConfig:
    """ Api keys for clients. """

    yandex_geocoder_api_key: str
    yandex_weather_api_key: str
    open_weather_api_key: str


@dataclass
class DatabaseConfig:
    """ Config data for database. """

    database_csv_file_path: str
    database_resources_path: str


@dataclass
class ResourceConfig:
    """ Config data for recourse management. """

    upload_dir: str
    upload_meta_data_file_path: str


@dataclass
class Config:
    """ Project configuration data. """

    database: DatabaseConfig
    resource: ResourceConfig
    clients: ClientConfig


def load_config(config_dir: str) -> Config:
    """ Load project config from 'config.json' file in given config_dir.
    :param config_dir: path where 'config.json' file is stored
    :return: project config
    """

    with open(os.path.join(config_dir, 'config.json'), "r") as config_file:
        # Load config
        config_json = json.load(config_file)

        # Parse config
        return from_dict(data_class=Config, data=config_json)
