from dataclasses import dataclass

from typing import List, Optional


@dataclass
class MainWeatherInfo:
    temp: float
    feels_like: float
    pressure: int
    humidity: int
    temp_min: float
    temp_max: float


@dataclass
class WindInfo:
    speed: float
    deg: int
    gust: Optional[float]


@dataclass
class CloudsInfo:
    all: int


@dataclass
class WeatherInfo:
    id: int


@dataclass
class WeatherFullInfo:
    dt: int
    main: MainWeatherInfo
    wind: WindInfo
    clouds: CloudsInfo
    weather: List[WeatherInfo]


@dataclass
class OpenWeatherResponse:
    message: Optional[str]
    cod: Optional[str]
    city_id: Optional[int]
    calctime: Optional[float]
    cnt: Optional[int]
    list: Optional[List[WeatherFullInfo]]
