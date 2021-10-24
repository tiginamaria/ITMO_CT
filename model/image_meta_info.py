import datetime as datetime
from dataclasses import dataclass
from enum import Enum
from typing import Optional, List, Any


class MetaDataKey(str, Enum):
    """ Dict fields in image meta data. """
    IMAGE_NAME = 'image_name'
    DATETIME = 'datetime'
    LOCATION = 'location'
    ADDRESS = 'address'


@dataclass
class ImageMetaInfo:
    """ Class which holds meta all information about image, when exif data is not provided. """

    image_name: str
    location: Optional[List[float]]
    address: Optional[str]
    date_time: Any

    def __post_init__(self):
        self.date_time = datetime.datetime.fromisoformat(self.date_time)


@dataclass
class MetaDataInfo:
    """ Class which holds meta information about all uploading images, fow which exif data is not provided. """

    meta_info: List[ImageMetaInfo]
