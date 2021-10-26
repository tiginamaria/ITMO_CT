import datetime as datetime
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import List, Tuple

from PIL import Image

from clients.openweather.openweather_client import OpenWeatherClient
from clients.yandex_geocoder.yandex_geocoder_client import YandexGeocoderClient
from database.database_sqlite import ImageDatabase
from image_processing.color_processing import get_color_info
from image_processing.exif_processing import get_exif_info_from_image, read_exif_info
from image_processing.weather_processing import get_weather_info
from model.image_colors_info import ImageColorsInfo
from model.image_exif_info import ImageExifInfo
from model.image_info import ImageInfo
from utils.config import load_config
from utils.image_file_utils import get_image_extension, get_image_name, create_dir, remove_dir, get_parent_path

PROJECT_DIR = Path(__file__).parents[1]
RESOURCES_DIR = PROJECT_DIR / 'resources'


class ImageDatabaseSQLiteClient:

    def __init__(self):
        config = load_config(RESOURCES_DIR)
        self._db = ImageDatabase(os.path.join(PROJECT_DIR, config.database.database_db_file_path))
        self._image_resource_path = os.path.join(PROJECT_DIR, config.database.database_resources_path)
        self._image_processing_executor = ThreadPoolExecutor(max_workers=1)

        self._geocoder_client = YandexGeocoderClient(config.clients.yandex_geocoder_api_key)
        self._open_weather_client = OpenWeatherClient(config.clients.open_weather_api_key)

    def _get_image_resource_dir(self, image_id: int) -> str:
        return os.path.join(self._image_resource_path, f'image_{image_id}')

    def _get_image_file(self, image_id: int) -> str:
        image_resources_dir = self._get_image_resource_dir(image_id)
        image_name = self._db.get_image_name_by_entry_id(image_id)
        image_file = os.path.join(image_resources_dir, image_name)
        return image_file

    def _add_images_to_database(self, image_paths: List[str]) -> List[int]:
        image_ids = []
        logging.info(f'Start to add images to database')
        for image_path in image_paths:
            logging.info(f'Adding image {image_path}')

            # Check given file by path exists
            if not os.path.exists(image_path):
                logging.warning(f"File {image_path} do not exist")
                continue

            # Check given file by path is image (has extensions .png, .jpeg, .jpg)
            image_name = get_image_name(image_path)
            if get_image_extension(image_name) is None:
                logging.warning(f"File {image_name} is not an image")
                continue

            # Save image to database
            image_id = self._db.add_new_image(image_name)
            image_ids.append(image_id)

            # Create directory for new image in resources directory
            image_resources_dir = self._get_image_resource_dir(image_id)
            create_dir(image_resources_dir)

            # Copy image to resources directory
            image = Image.open(image_path)
            image.save(os.path.join(image_resources_dir, image_name), quality=20, optimize=True)
            logging.info(f"File {image_path} was saved to database with id {image_id}")

        logging.info(f'Finish to add images to database')
        return image_ids

    def _add_exif_info_for_image(self, image_id: int):
        image_file = self._get_image_file(image_id)

        # Extracting exif information
        logging.info(f"Extracting exif information from image: {image_id}")
        exif_info = get_exif_info_from_image(image_file)

        # If there is no exif data try to read it from user
        if exif_info is None:
            logging.info(f"Can not get exif info for image: {image_id}")
            exif_info = read_exif_info(image_file, self._geocoder_client)

            # If user data is not correct return
            if exif_info is None:
                raise Exception(f"Failed to get or read exif info for image: {image_id}")

        # Add exif info to database
        self._db.add_exif_info(image_id, exif_info)

    def _add_weather_info_for_image(self, image_id: int):
        gps_info = self._db.get_gps_info_by_entry_id(image_id)
        date_time_info = self._db.get_datetime_by_entry_id(image_id)

        # Extracting weather information
        logging.info(f"Extracting weather information from image: {image_id}")
        weather_info = get_weather_info(gps_info.location(), date_time_info.date_time, self._open_weather_client)

        # If there is no weather info try to read it from user
        if weather_info is None:
            logging.info(f"Can not get weather info for image: {image_id}")
            image_file = self._get_image_file(image_id)
            # weather_info = read_weather_info(image_file)

            # If user data is not correct return
            if weather_info is None:
                raise Exception(f"Failed to get or read weather info for image: {image_id}")

        # Add weather info to database
        self._db.add_weather_info(image_id, weather_info)

    def _add_color_info_for_image(self, image_id: int):
        image_file = self._get_image_file(image_id)

        # Extracting color information
        logging.info(f"Extracting color information from image: {image_id}")
        color_info = get_color_info(image_file)

        # Add colors info to database
        for color in color_info.colors:
            self._db.add_color_info(image_id, color)

    def _add_images_info_to_database(self, image_ids: List[int]) -> List[int]:
        processed_image_ids = []
        logging.info(f'Start to add images infos to database')
        for image_id in image_ids:
            logging.info(f'Start processing image {image_id}')

            try:
                self._add_exif_info_for_image(image_id)
                self._add_weather_info_for_image(image_id)
                self._add_color_info_for_image(image_id)

            except Exception as e:
                logging.error(f'Skipping image {image_id} due to error:', e)
                self._db.delete_image_by_entry_id(image_id)
                remove_dir(self._get_image_resource_dir(image_id))
                continue

            processed_image_ids.append(image_id)
            logging.info(f'Finish processing image {image_id}')

        logging.info(f'Finish to add images infos to database')
        return processed_image_ids

    def add_images(self, image_paths: List[str]):
        added_image_ids = self._add_images_to_database(image_paths)
        print(f'{len(added_image_ids)}/{len(image_paths)} have been successfully uploaded')

        # TODO: Make operation async
        processed_image_ids = self._add_images_info_to_database(added_image_ids)
        print(f'{len(processed_image_ids)}/{len(added_image_ids)} have been successfully processed')

    def get_images(self,
                   location: Tuple[float, float],
                   date_time: datetime.datetime,
                   weather: int,
                   hour_delta=3,
                   month_delta=1,
                   latitude_delta=0.5,
                   longitude_delta=0.5,
                   weather_delta=30) -> List[ImageInfo]:

        image_ids = self._db.get_entry_id_by_parameters(
            hour_interval_left=(date_time.hour - hour_delta + 24) % 24,
            hour_interval_right=(date_time.hour + hour_delta + 24) % 24,
            month_interval_left=(date_time.month - month_delta - 1) % 12 + 1,
            month_interval_right=(date_time.month + month_delta - 1) % 12 + 1,
            latitude_interval_left=location[0] - latitude_delta,
            latitude_interval_right=location[0] + latitude_delta,
            longitude_interval_left=location[1] - longitude_delta,
            longitude_interval_right=location[1] + longitude_delta,
            weather_interval_left=max(0, weather - weather_delta),
            weather_interval_right=min(100, weather + weather_delta),
        )

        images = []
        for image_id in image_ids:
            image_file = self._get_image_file(image_id)
            image_pallet = os.path.join(get_parent_path(image_file), 'palette.png')
            image_clusters = os.path.join(get_parent_path(image_file), 'clusters.png')

            image = ImageInfo(
                id=image_id,
                name=self._db.get_image_name_by_entry_id(image_id),
                exif_info=ImageExifInfo(
                    date_time_info=self._db.get_datetime_by_entry_id(image_id),
                    gps_info=self._db.get_gps_info_by_entry_id(image_id)
                ),
                weather_info=self._db.get_weather_info_by_entry_id(image_id),
                colors_info=ImageColorsInfo(self._db.get_colors_info_by_entry_id(image_id)),
                image_path=image_file,
                palette_path=image_pallet,
                clusters_path=image_clusters
            )
            images.append(image)
        return images
