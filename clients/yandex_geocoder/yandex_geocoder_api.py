from dataclasses import dataclass

from typing import Tuple, List


@dataclass
class GeocoderResponseMetaData:
    request: str
    results: int
    found: int


@dataclass
class MetaDataProperty:
    geocoder_response_meta_data: GeocoderResponseMetaData


@dataclass
class Point:
    pos: str

    def to_lat_lon(self) -> Tuple[float, float]:
        lon, lat = map(float, self.pos.split(' '))
        return lat, lon


@dataclass
class GeoObject:
    name: str
    point: Point


@dataclass
class GeoObjectWrapper:
    geo_object: GeoObject


@dataclass
class GeoObjectCollection:
    meta_data_property: MetaDataProperty
    feature_member: List[GeoObjectWrapper]


@dataclass
class YandexGeocoderResponse:
    geo_object_collection: GeoObjectCollection
