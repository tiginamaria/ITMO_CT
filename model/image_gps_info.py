from dataclasses import dataclass

from typing import List, Union, Tuple


@dataclass(frozen=True)
class ImageGPSInfo:
    lat: float
    lon: float

    @staticmethod
    def _from_rational64u(location: List[float], direction: str) -> float:
        degrees, minutes, seconds = map(float, location)
        direction_to_coef = {'N': 1, 'S': -1, 'E': 1, 'W': -1}
        return (degrees + minutes / 60 + seconds / 3600) * direction_to_coef[direction]

    @staticmethod
    def from_exif_data(gps_data_list: List[Union[List[float], str]]) -> 'ImageGPSInfo':
        return ImageGPSInfo(
            lat=ImageGPSInfo._from_rational64u(gps_data_list[2], gps_data_list[1]),
            lon=ImageGPSInfo._from_rational64u(gps_data_list[4], gps_data_list[3]),
        )

    def location(self) -> Tuple[float, float]:
        return self.lat, self.lon

    @classmethod
    def from_row(cls, row) -> 'ImageGPSInfo':
        return ImageGPSInfo(row[0], row[1])
