from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import pandas as pd

from database.model.columns import ExifInfoColumnName


class Season(str, Enum):
    WINTER = 'winter'
    SPRING = 'spring'
    SUMMER = 'summer'
    AUTUMN = 'autumn'

    @staticmethod
    def from_month(month: int) -> 'Season':
        if month <= 3:
            return Season.WINTER
        if month <= 6:
            return Season.SPRING
        if month <= 9:
            return Season.SUMMER
        if month <= 12:
            return Season.AUTUMN


@dataclass(frozen=True)
class DataTimeInfo:
    season: Season
    date_time: datetime

    @staticmethod
    def from_exif_data(data_time_str) -> 'DataTimeInfo':
        # Parse data_time from exif data by format %Y:%m:%d %H:%M:%S
        date_time = datetime.strptime(data_time_str, '%Y:%m:%d %H:%M:%S')

        return DataTimeInfo(
            season=Season.from_month(date_time.month),
            date_time=date_time
        )

    @classmethod
    def from_row(cls, row: pd.Series) -> 'DataTimeInfo':
        return DataTimeInfo(
            season=Season(row[ExifInfoColumnName.SEASON]),
            date_time=datetime.fromisoformat(row[ExifInfoColumnName.DATETIME])
        )

    def to_json(self):
        return {
            ExifInfoColumnName.SEASON: self.season,
            ExifInfoColumnName.DATETIME: self.date_time,
        }

    @classmethod
    def from_datetime(cls, date_time: datetime) -> 'DataTimeInfo':
        return DataTimeInfo(
            season=Season.from_month(date_time.month),
            date_time=date_time
        )
