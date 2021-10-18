from dataclasses import dataclass

from typing import List, Union
import pandas as pd

from database.model.columns import ExifInfoColumnName


@dataclass(frozen=True)
class GPSInfo:
    latitude: float
    longitude: float

    @staticmethod
    def from_rational64u(location: List[float], direction: str) -> float:
        degrees, minutes, seconds = map(float, location)
        direction_to_coef = {'N': 1, 'S': -1, 'E': 1, 'W': -1}
        return (degrees + minutes / 60 + seconds / 3600) * direction_to_coef[direction]

    @staticmethod
    def from_exif_data(gps_data_list: List[Union[List[float], str]]) -> 'GPSInfo':
        return GPSInfo(
            latitude=GPSInfo.from_rational64u(gps_data_list[2], gps_data_list[1]),
            longitude=GPSInfo.from_rational64u(gps_data_list[4], gps_data_list[3]),
        )

    @classmethod
    def from_row(cls, row: pd.Series) -> 'GPSInfo':
        return GPSInfo(
            latitude=row[ExifInfoColumnName.LATITUDE],
            longitude=row[ExifInfoColumnName.LONGITUDE]
        )

    def to_json(self):
        return {
            ExifInfoColumnName.LATITUDE: self.latitude,
            ExifInfoColumnName.LONGITUDE: self.longitude,
        }
