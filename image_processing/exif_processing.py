import logging
from datetime import datetime
from typing import Optional

from PIL import Image
from PIL.ExifTags import TAGS

from clients.yandex_geocoder.yandex_geocoder_client import YandexGeocoderClient
from model.image_datatime_info import ImageDateTimeInfo
from model.image_exif_info import ImageExifInfo, ExifDataKey
from model.image_gps_info import ImageGPSInfo
from utils.image_file_utils import get_image_name


def get_exif_info_from_image(image_file: str) -> Optional[ImageExifInfo]:
    """
    Method extracts exif data from image.
    :param image_file: path to image to extract exif data
    :return: exif information
    """

    # Opening the image
    image = Image.open(image_file)

    # Extracting the exif metadata
    exif_data = image.getexif()

    # Creating image exif data dictionary
    exif_data_dict = {}

    # Looping through all the tags present in exif data
    for tag_key, tag_value in exif_data.items():
        # Getting the tag name instead of tag id
        tag_name = TAGS.get(tag_key, tag_key)

        # Adding new entry to the dictionary
        exif_data_dict[tag_name] = tag_value

    if ExifDataKey.GPS_INFO in exif_data_dict and ExifDataKey.GPS_INFO in exif_data_dict:
        return ImageExifInfo.from_exif_data(exif_data_dict)
    else:
        logging.warning("DateTime and GPSInfo not provided in image exif data.")
        return None


def read_exif_info(image_file: str, geocoder_client: YandexGeocoderClient) -> Optional[ImageExifInfo]:
    image_name = get_image_name(image_file)
    image = Image.open(image_file)
    # image.show()
    print(f"Service can not detect where {image_name} was made?")
    print(f"Please, enter address (e.x. Ленинский пр. 161, 13) or location (e.x. 30.23 60.132) for it:")
    result = input()
    try:
        location = list(map(float, result.split(' ')))
        print(f"Got location: {location[0], location[1]}")
    except Exception:
        location = geocoder_client.get_location_by_address(result)
        if location is None:
            logging.error(f"Can not get location for address {result}")
            # image.close()
            return None

        print(f"Got address: {result}, detect location {location[0], location[1]}")

    print(f"Please, enter datetime (e.x. 2021-10-25 09:31:32) for it:")
    result = input()
    try:
        date_time = datetime.fromisoformat(result)
        print(f"Got datetime: {date_time}")
    except Exception:
        logging.error(f"Can not get datetime from string {result}")
        # image.close()
        return None

    image.close()
    return ImageExifInfo(ImageDateTimeInfo.from_datetime(date_time), ImageGPSInfo(location[0], location[1]))
