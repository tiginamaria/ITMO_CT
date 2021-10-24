import logging
import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import List

from PIL import Image

from utils.config import load_config
from utils.image_file_utils import get_image_extension, copy_image, get_image_name, create_dir
from database.database_sqlite import ImageDatabase
from image_processing.color_processing import get_color_info
from image_processing.exif_processing import extract_exif_info_from_image
from image_processing.weather_processing import get_weather_data
from model.image_info import ImageInfo

PROJECT_DIR = Path(__file__).parents[1]
RESOURCES_DIR = PROJECT_DIR / 'resources'


class ImageDatabaseSQLiteClient:

    def __init__(self):
        self._config = load_config(RESOURCES_DIR)
        self._db = ImageDatabase(os.path.join(PROJECT_DIR, self._config.database.database_db_file_path))
        self._image_resource_path = os.path.join(PROJECT_DIR, self._config.database.database_resources_path)
        self._image_processing_executor = ThreadPoolExecutor(max_workers=1)

    def _get_image_resource_dir(self, entity_id: int) -> str:
        return os.path.join(self._image_resource_path, f'image_{entity_id}')

    def _add_images_to_database(self, new_image_paths: List[str]) -> List[int]:
        entity_ids = []
        logging.info(f'Start to add images to database')
        for new_image_path in new_image_paths:
            logging.info(f'Adding image {new_image_path}')
            if not os.path.exists(new_image_path):
                logging.warning(f"File {new_image_path} do not exist")
                continue

            new_image_name = get_image_name(new_image_path)
            if get_image_extension(new_image_name) is None:
                logging.warning(f"File {new_image_name} is not an image")
                continue

            new_entity_id = self._db.add_new_image(new_image_name)
            entity_ids.append(new_entity_id)

            # Create directory for new image in resources directory
            image_resources_dir = self._get_image_resource_dir(new_entity_id)
            create_dir(image_resources_dir)

            # Copy image to resources directory
            logging.info(f"File {new_image_name} is not an image")
            copy_image(new_image_path, image_resources_dir)
        logging.info(f'Finish to add images to database')
        return entity_ids

    def _add_images_info_to_database(self, entity_ids: List[int]) -> List[ImageInfo]:
        images = []
        logging.info(f'Start to add images infos to database')

        for entity_id in entity_ids:

            image_resources_dir = self._get_image_resource_dir(entity_id)
            image_name = self._db.get_image_name_by_entry_id(entity_id)
            image_file = os.path.join(image_resources_dir, image_name)

            # Opening the image
            image = Image.open(image_file)

            # Extracting exif information
            # TODO: add images meta file to extract data from there if there is no exif data
            logging.info(f"Extracting exif information from image: {image_name}")
            exif_info = extract_exif_info_from_image(image)
            if exif_info is None:
                logging.info(f"Can not get exif info for image: {image_file}")
            else:
                self._db.add_datetime(entity_id, exif_info.data_time.date_time)
                self._db.add_location(entity_id, exif_info.gps_info.latitude, exif_info.gps_info.longitude)

            # Extracting weather information
            logging.info(f"Extracting weather information from image: {image_name}")
            weather_info = get_weather_data(exif_info, self._config.clients.open_weather_api_key)
            if weather_info is None:
                logging.info(f"Can not get weather info for image: {image_file}")
            else:
                self._db.add_weather(entity_id, weather_info.clouds)

            # Extracting color information
            logging.info(f"Extracting color information from image: {image_name}")
            color_info = get_color_info(image, image_resources_dir)
            for color in color_info.colors:
                self._db.add_color(entity_id, color.r, color.g, color.b, int(color.percent * 100))

            images.append(ImageInfo(image_name, exif_info, weather_info, color_info, path=image_resources_dir))

        logging.info(f'Finish to add images infos to database')
        return images

    def add_all_images(self, new_image_paths: List[str]):
        entity_ids = self._add_images_to_database(new_image_paths)
        print(f'{len(entity_ids)}/{len(new_image_paths)} have been successfully uploaded')
        # TODO: Make operation async
        images = self._add_images_info_to_database(entity_ids)
        print(f'{len(images)}/{len(entity_ids)} have been successfully processed')
