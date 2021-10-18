import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict

import logging
from PIL import Image

from core.utils.config import load_config
from database.database_client import ImageDatabaseCSVClient
from image_processing.color_processing import get_color_info
from image_processing.exif_processing import extract_exif_info_from_image
from core.utils.image_file_utils import get_image_extension, copy_image, create_dir, remove_dir
from image_processing.weather_processing import get_weather_data
from model.image_exif_info import ExifDataKey
from model.image_info import ImageInfo

PROJECT_DIR = Path(__file__).parents[1]
RESOURCES_DIR = PROJECT_DIR / 'resources'
TEMPORARY_DIR = RESOURCES_DIR / 'tmp'


def upload_images(meta: Dict[str, Any] = None):
    if meta is None:
        meta = {}

    config = load_config(RESOURCES_DIR)
    image_files = os.scandir(os.path.join(PROJECT_DIR, config.resource.upload_dir))
    images = []

    # Create temporary directory for images information
    try:
        create_dir(TEMPORARY_DIR)
        for i, image_file in enumerate(image_files):
            try:
                if get_image_extension(image_file.name) is not None:
                    logging.info(f'Start to load image: {image_file.name}')

                    # Create temporary directory for image information
                    tmp_image_dir = os.path.join(TEMPORARY_DIR, f'image_{i}')
                    create_dir(tmp_image_dir)

                    # Copy image to temporary directory
                    tmp_image_file = os.path.join(tmp_image_dir, image_file.name)
                    copy_image(image_file.path, tmp_image_dir)

                    # Opening the image
                    image = Image.open(tmp_image_file)

                    # Extracting exif information
                    exif_info = extract_exif_info_from_image(image, meta.get(image_file.name, None))

                    # Extracting weather information
                    weather_info = get_weather_data(exif_info)

                    # Extracting color information
                    color_info = get_color_info(image, tmp_image_dir)

                    images.append(ImageInfo(tmp_image_dir, exif_info, weather_info, color_info))

                    logging.info(f'Finish to load image: {image_file.name}')

            except Exception as e:
                logging.error(f'Failed to load image: {image_file.name}: {e}', e)

        # Save images to database
        database_client = ImageDatabaseCSVClient(os.path.join(PROJECT_DIR, config.database.database_csv_file_path),
                                                 os.path.join(PROJECT_DIR, config.database.database_resources_path))
        database_client.add_all_images(images)

    # except Exception as e:
    #     logging.error(f'Failed to load images: {e}')
    #
    finally:
        # Remove temporary directory for images information
        remove_dir(TEMPORARY_DIR)


if __name__ == '__main__':
    upload_images({
        'photo_2021-10-10 12.19.05.jpg': {
            ExifDataKey.DATETIME: datetime.now() - timedelta(days=10),
            ExifDataKey.LOCATION: (60, 30)
        }
    })