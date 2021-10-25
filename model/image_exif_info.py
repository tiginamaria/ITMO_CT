from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any

import pandas as pd

from model.image_datatime_info import DateTimeInfo
from model.image_gps_info import GPSInfo
from model.image_meta_info import ImageMetaInfo


class ExifDataKey(str, Enum):
    """ Dict fields in image exif data. """
    DATETIME = 'DateTime'
    GPS_INFO = 'GPSInfo'


@dataclass(frozen=True)
class ImageExifInfo:
    """ Class which holds all information about image. """

    data_time: DateTimeInfo
    gps_info: GPSInfo

    @staticmethod
    def from_exif_data(exif_data: Dict[str, Any]) -> 'ImageExifInfo':
        """ Parse exif information from dict with exif data.
        :param exif_data: extracted from image dict with exif data
        :return: exif information
        """

        return ImageExifInfo(
            data_time=DateTimeInfo.from_string(exif_data[ExifDataKey.DATETIME]),
            gps_info=GPSInfo.from_exif_data(exif_data[ExifDataKey.GPS_INFO]),
        )

    @staticmethod
    def from_meta_info(meta_info: ImageMetaInfo) -> 'ImageExifInfo':
        """ Parse exif information from dict with meta data.
        :param meta_info: image dict with meta data
        :return: exif information
        """

        return ImageExifInfo(
            data_time=DateTimeInfo.from_datetime(meta_info.date_time),
            gps_info=GPSInfo(meta_info.location[0], meta_info.location[1]),
        )

    @classmethod
    def from_row(cls, row: pd.Series) -> 'ImageExifInfo':
        """ Parse exif information from dataset raw.
        :param row: dataset raw to parse exif information from
        :return: exif information
        """
        return ImageExifInfo(
            data_time=DateTimeInfo.from_row(row),
            gps_info=GPSInfo.from_row(row)
        )

    def to_json(self):
        """ Damp exif information to dict.
        :return: dict with exif information
        """
        return {
            **self.data_time.to_json(),
            **self.gps_info.to_json(),
        }
