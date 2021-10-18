import datetime
import json
import logging
import os
from typing import Dict

from dacite import from_dict, Config

from clients.yandex_geocoder.yandex_geocoder_client import YandexGeocoderClient
from model.image_meta_info import ImageMetaInfo, MetaDataInfo


def meta_processing(meta_info_file_path: str, api_key: str) -> Dict[str, ImageMetaInfo]:
    """ Get location by given meta data for image.
    :param meta_info_file_path: path to meta info file for image uploading
    :param api_key: geocoder api key
    :return: image weather information
    """

    if not os.path.exists(meta_info_file_path):
        return {}

    client = YandexGeocoderClient(api_key)

    with open(meta_info_file_path, "r") as meta_info_file:
        # Load config
        meta_info_json = json.load(meta_info_file)

    # Parse config
    meta_data_info = from_dict(data_class=MetaDataInfo, data=meta_info_json)

    # Here image meta information by image name will be collected
    image_name_to_meta = {}
    for image_meta_info in meta_data_info.meta_info:

        if image_meta_info.location is None and image_meta_info.address is None:
            logging.warning(
                f"Both location and address not provided in meta info for image {image_meta_info.image_name}")
            continue

        if image_meta_info.location is None:
            location = client.get_location_by_address(image_meta_info.address)
            if location is None:
                logging.warning(
                    f"Can not get location for given address {image_meta_info.address} for image {image_meta_info.image_name}")
                continue
            else:
                image_meta_info.location = location

        image_name_to_meta[image_meta_info.image_name] = image_meta_info

    return image_name_to_meta
