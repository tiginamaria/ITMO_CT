from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any

from model.image_datatime_info import ImageDateTimeInfo
from model.image_gps_info import ImageGPSInfo


class ExifDataKey(str, Enum):
    """ Dict fields in image exif data. """
    DATETIME = 'DateTime'
    GPS_INFO = 'GPSInfo'


@dataclass(frozen=True)
class ImageExifInfo:
    """ Class which holds all information about image. """

    date_time_info: ImageDateTimeInfo
    gps_info: ImageGPSInfo

    @staticmethod
    def from_exif_data(exif_data: Dict[str, Any]) -> 'ImageExifInfo':
        """ Parse exif information from dict with exif data.
        :param exif_data: extracted from image dict with exif data
        :return: exif information
        """

        return ImageExifInfo(
            date_time_info=ImageDateTimeInfo.from_string(exif_data[ExifDataKey.DATETIME]),
            gps_info=ImageGPSInfo.from_exif_data(exif_data[ExifDataKey.GPS_INFO]),
        )
