import os
from typing import List

import pandas as pd

from core.utils.image_file_utils import get_image_extension, copy_image
from database.model.columns import COLUMNS_NAMES
from model.image_info import ImageInfo


class ImageDatabaseClient:

    def get_all_images(self) -> List[ImageInfo]:
        pass

    def add_all_images(self, new_images: List[ImageInfo]):
        pass


class ImageDatabaseCSVClient(ImageDatabaseClient):

    def __init__(self, image_database_path: str, image_resource_path: str):
        self.image_database_path = image_database_path
        self.image_resource_path = image_resource_path

        if os.path.getsize(self.image_database_path) == 0:
            self._init_database()

    def _init_database(self):
        df = pd.DataFrame([], columns=COLUMNS_NAMES)
        df.to_csv(self.image_database_path, index=False)

    def get_all_images(self) -> List[ImageInfo]:
        df_image = pd.read_csv(self.image_database_path)
        images = []
        for i, image in df_image.iterrows():
            images.append(ImageInfo.from_row(image))
        return images

    def add_all_images(self, new_images: List[ImageInfo]):
        df_image = pd.read_csv(self.image_database_path)
        image_last_id = df_image.shape[0]

        for i, new_image in enumerate(new_images):
            new_image.id = image_last_id + i
            new_image.path = self._save_image(new_image)

        df_image = pd.read_csv(self.image_database_path)
        df_new_image = pd.DataFrame.from_records([new_image.to_json() for new_image in new_images])
        df_image = pd.concat([df_image, df_new_image])
        df_image.to_csv(self.image_database_path, index=False)

    def _save_image(self, new_images: ImageInfo) -> str:
        new_image_dir = os.path.join(self.image_resource_path, f'image_{new_images.id}')
        os.makedirs(os.path.join(new_image_dir))

        new_image_files = os.scandir(new_images.path)
        for new_image_file in new_image_files:
            if get_image_extension(new_image_file.name) is not None:
                copy_image(new_image_file.path, new_image_dir)

        return new_image_dir
