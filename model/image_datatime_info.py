from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class ImageDateTimeInfo:
    date_time: datetime

    @staticmethod
    def from_string(data_time_str) -> 'ImageDateTimeInfo':
        # Parse data_time from exif data by format %Y:%m:%d %H:%M:%S
        date_time = datetime.strptime(data_time_str, '%Y:%m:%d %H:%M:%S')

        return ImageDateTimeInfo(
            date_time=date_time
        )

    @classmethod
    def from_datetime(cls, date_time: datetime) -> 'ImageDateTimeInfo':
        return ImageDateTimeInfo(
            date_time=date_time
        )

    @classmethod
    def from_row(cls, row) -> 'ImageDateTimeInfo':
        return cls.from_datetime(datetime.fromisoformat(row[0]))
