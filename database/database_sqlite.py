import sqlite3
from datetime import datetime
from typing import List

from model.image_colors_info import ImageColorInfo
from model.image_datatime_info import ImageDateTimeInfo
from model.image_exif_info import ImageExifInfo
from model.image_gps_info import ImageGPSInfo
from model.image_weather_info import ImageWeatherInfo


class ImageDatabase:

    def __init__(self, database_path):

        self.db_path = database_path

    # Filling functions

    def add_new_image(self, photo_name: str, photo_hash: str) -> int:

        current_dt = datetime.utcnow()
        current_dt = str(current_dt).split('.')[0]

        self._open_database()
        result = self.cursor.execute("INSERT INTO Photos (PhotoName, PhotoHash, UploadDateTime) VALUES (?, ?, ?)",
                                     (photo_name, photo_hash, current_dt))
        entry_id = result.lastrowid
        self._close_database()

        return entry_id

    def add_exif_info(self, entry_id: int, exif_info: ImageExifInfo):

        self._open_database()
        self.cursor.execute("UPDATE Photos SET PhotoDateTime=?, LocationLatitude=?, LocationLongitude=? "
                            "WHERE PhotoID=?", (exif_info.date_time_info.date_time,
                                                exif_info.gps_info.lat, exif_info.gps_info.lon, entry_id))
        self._close_database()

    def add_datetime_info(self, entry_id: int, datetime_info: ImageDateTimeInfo):

        self._open_database()
        self.cursor.execute("UPDATE Photos SET PhotoDateTime=? WHERE PhotoID=?", (datetime_info.date_time, entry_id))
        self._close_database()

    def add_gps_info(self, entry_id: int, gps_info: ImageGPSInfo):

        self._open_database()
        self.cursor.execute("UPDATE Photos SET LocationLatitude=?, LocationLongitude=? WHERE PhotoID=?",
                            (gps_info.lat, gps_info.lon, entry_id))
        self._close_database()

    def add_weather_info(self, entry_id: int, weather: ImageWeatherInfo):

        self._open_database()
        self.cursor.execute("UPDATE Photos SET Weather=? WHERE PhotoID=?", (weather.clouds, entry_id))
        self._close_database()

    def add_color_info(self, entry_id: int, image_colo_info: ImageColorInfo):

        self._open_database()
        self.cursor.execute(
            "INSERT INTO Colors (PhotoID, ColorRed, ColorGreen, ColorBlue, ColorPercentage) VALUES (?, ?, ?, ?, ?)",
            (entry_id, image_colo_info.r, image_colo_info.g, image_colo_info.b, image_colo_info.percent))
        self._close_database()

    # Request functions

    def get_all_image_names(self):

        self._open_database()
        result = self.cursor.execute("SELECT PhotoName FROM Photos")
        result = result.fetchall()
        self._close_database()

        return result

    def get_image_name_by_exact_color(self, red_value: float, green_value: float, blue_value: float):

        self._open_database()
        result = self.cursor.execute(
            "SELECT PhotoName FROM Photos WHERE PhotoID IN (SELECT PhotoID FROM Colors WHERE ColorRed=? AND ColorGreen=? AND ColorBlue=?)",
            (red_value, green_value, blue_value))
        result = result.fetchall()
        self._close_database()

        return result

    def get_entry_id_by_parameters(self, hour_interval_left: int, hour_interval_right: int,
                                   month_interval_left: int, month_interval_right: int,
                                   latitude_interval_left: float, latitude_interval_right: float,
                                   longitude_interval_left: float, longitude_interval_right: float,
                                   weather_interval_left: int, weather_interval_right: int) -> List[int]:

        request_text = "SELECT PhotoID FROM Photos WHERE TRUE"

        if hour_interval_left > hour_interval_right:
            request_text += " AND ((cast(strftime('%H', time(PhotoDateTime)) as INTEGER) >= {})" \
                            " OR (cast(strftime('%H', time(PhotoDateTime)) as INTEGER) <= {}))" \
                .format(hour_interval_left, hour_interval_right)
        else:
            request_text += " AND (cast(strftime('%H', time(PhotoDateTime)) as INTEGER) BETWEEN {} AND {})" \
                .format(hour_interval_left, hour_interval_right)

        if month_interval_left > month_interval_right:
            request_text += " AND ((cast(strftime('%m', date(PhotoDateTime)) as INTEGER) >= {})" \
                            " OR (cast(strftime('%m', date(PhotoDateTime)) as INTEGER) <= {}))" \
                .format(month_interval_left, month_interval_right)
        else:
            request_text += " AND (cast(strftime('%m', date(PhotoDateTime)) as INTEGER) BETWEEN {} AND {})" \
                .format(month_interval_left, month_interval_right)

        request_text += " AND (LocationLatitude BETWEEN {} AND {})" \
            .format(latitude_interval_left, latitude_interval_right)
        request_text += " AND (LocationLongitude BETWEEN {} AND {})" \
            .format(longitude_interval_left, longitude_interval_right)
        request_text += " AND (Weather BETWEEN {} AND {})" \
            .format(weather_interval_left, weather_interval_right)

        print(request_text)

        self._open_database()
        result = self.cursor.execute(request_text)
        result = result.fetchall()
        self._close_database()

        result_list = []
        for row in result:
            result_list.append(row[0])

        return result_list

    def get_image_name_by_entry_id(self, entry_id: int) -> str:

        self._open_database()
        result = self.cursor.execute("SELECT PhotoName FROM Photos WHERE PhotoID=?", (entry_id,))
        result = result.fetchall()
        self._close_database()

        for row in result:
            return row[0]

    def get_gps_info_by_entry_id(self, entry_id: int) -> ImageGPSInfo:

        self._open_database()
        result = self.cursor.execute("SELECT LocationLatitude, LocationLongitude FROM Photos WHERE PhotoID=?",
                                     (entry_id,))
        result = result.fetchall()
        self._close_database()

        for row in result:
            return ImageGPSInfo.from_row(row)

    def get_datetime_by_entry_id(self, entry_id: int) -> ImageDateTimeInfo:

        self._open_database()
        result = self.cursor.execute("SELECT datetime(PhotoDateTime) FROM Photos WHERE PhotoID=?",
                                     (entry_id,))
        result = result.fetchall()
        self._close_database()

        for row in result:
            return ImageDateTimeInfo.from_row(row)

    def get_weather_info_by_entry_id(self, entry_id: int) -> ImageWeatherInfo:

        self._open_database()
        result = self.cursor.execute("SELECT Weather FROM Photos WHERE PhotoID=?",
                                     (entry_id,))
        result = result.fetchall()
        self._close_database()

        for row in result:
            return ImageWeatherInfo.from_row(row)

    def get_colors_info_by_entry_id(self, entry_id: int) -> List[ImageColorInfo]:

        self._open_database()
        result = self.cursor.execute(
            "SELECT ColorRed, ColorGreen, ColorBlue, ColorPercentage FROM Colors WHERE PhotoID=?", (entry_id,))
        result = result.fetchall()
        self._close_database()

        colors = []
        for row in result:
            colors.append(ImageColorInfo.from_row(row))
        return colors

    def delete_image_by_entry_id(self, entry_id: int):
        self._delete_entry(entry_id)

    # Service functions

    def _open_database(self):

        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()

    def _close_database(self):

        self.connection.commit()
        self.connection.close()

    def _delete_entry(self, entry_id: int):

        self._open_database()
        self.cursor.execute("DELETE FROM Photos WHERE PhotoID=?", (entry_id,))
        self._close_database()

    def _get_all_entries(self, table_name: str):

        self._open_database()
        self.cursor.execute("SELECT * FROM {}".format(table_name))
        entries = self.cursor.fetchall()
        self._close_database()

        return entries
