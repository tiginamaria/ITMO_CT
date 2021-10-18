import logging
import os
from pathlib import Path

from PIL import Image

from core.utils.config import load_config
from core.utils.image_file_utils import get_image_extension, copy_image, create_dir, remove_dir
from database.database_client import ImageDatabaseCSVClient
from image_processing.color_processing import get_color_info
from image_processing.exif_processing import extract_exif_info_from_image
from image_processing.meta_processing import meta_processing
from image_processing.weather_processing import get_weather_data
from model.image_info import ImageInfo

PROJECT_DIR = Path(__file__).parents[1]
RESOURCES_DIR = PROJECT_DIR / 'resources'
TEMPORARY_DIR = RESOURCES_DIR / 'tmp'


def upload_images():
    """ Upload images from 'upload_dir' defined in project config file. """

    config = load_config(RESOURCES_DIR)
    meta_info = meta_processing(os.path.join(PROJECT_DIR, config.resource.upload_meta_data_file_path),
                                config.clients.yandex_geocoder_api_key)

    image_files = os.scandir(os.path.join(PROJECT_DIR, config.resource.upload_dir))
    images = []

    try:
        # Create temporary directory for images information
        create_dir(TEMPORARY_DIR)
        for i, image_file in enumerate(filter(lambda f: get_image_extension(f.name) is not None, image_files)):
            image_name, image_path = image_file.name, image_file.path
            try:
                logging.info(f'Start to load image: {image_name}')

                # Create temporary directory for image information
                tmp_image_dir = os.path.join(TEMPORARY_DIR, f'image_{i}')
                create_dir(tmp_image_dir)

                # Copy image to temporary directory
                tmp_image_file = os.path.join(tmp_image_dir, image_name)
                copy_image(image_path, tmp_image_dir)

                # Opening the image
                image = Image.open(tmp_image_file)

                # Extracting exif information
                exif_info = extract_exif_info_from_image(image, meta_info.get(image_name, None))

                # Extracting weather information
                weather_info = get_weather_data(exif_info, config.clients.open_weather_api_key)
                if weather_info is None:
                    raise Exception(f"Can not get weather info for image: {image_name}")

                # Extracting color information
                color_info = get_color_info(image, tmp_image_dir)

                images.append(ImageInfo(image_name, exif_info, weather_info, color_info, path=tmp_image_dir))

                logging.info(f'Finish to load image: {image_name}')

            except Exception as e:
                logging.error(f'Failed to load image: {image_name}: {e}', e)

        # Save images to database
        database_client = ImageDatabaseCSVClient(os.path.join(PROJECT_DIR, config.database.database_csv_file_path),
                                                 os.path.join(PROJECT_DIR, config.database.database_resources_path))
        database_client.add_all_images(images)
    except Exception as e:
        logging.error(f'Failed to load images: {e}')

    finally:
        # Remove temporary directory for images information
        remove_dir(TEMPORARY_DIR)


if __name__ == '__main__':
    upload_images()
