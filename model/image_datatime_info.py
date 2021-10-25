from dataclasses import dataclass
from datetime import datetime

import pandas as pd

from database.model.columns import ExifInfoColumnName


@dataclass(frozen=True)
class DateTimeInfo:
    date_time: datetime

    @staticmethod
    def from_string(data_time_str) -> 'DateTimeInfo':
        # Parse data_time from exif data by format %Y:%m:%d %H:%M:%S
        date_time = datetime.strptime(data_time_str, '%Y:%m:%d %H:%M:%S')

        return DateTimeInfo(
            date_time=date_time
        )

    @classmethod
    def from_row(cls, row: pd.Series) -> 'DateTimeInfo':
        return DateTimeInfo(
            date_time=datetime.fromisoformat(row[ExifInfoColumnName.DATETIME])
        )

    def to_json(self):
        return {
            ExifInfoColumnName.DATETIME: self.date_time,
        }

    @classmethod
    def from_datetime(cls, date_time: datetime) -> 'DateTimeInfo':
        return DateTimeInfo(
            date_time=date_time
        )
