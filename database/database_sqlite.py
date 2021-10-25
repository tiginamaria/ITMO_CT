# This file contains functions for database management

# Importing required modules
import sqlite3
from datetime import datetime

# Describing class for database operations
from typing import Tuple


class ImageDatabase:

    def __init__(self, database_path):

        self.db_path = database_path

    # Filling functions

    def add_new_image(self, photo_name: str):

        current_dt = datetime.utcnow()
        current_dt = str(current_dt).split('.')[0]

        self._open_database()
        result = self.cursor.execute("INSERT INTO Photos (PhotoName, UploadDateTime) VALUES (?, ?)",
                                     (photo_name, current_dt))
        entry_id = result.lastrowid
        self._close_database()

        return entry_id

    def add_datetime(self, entry_id: int, date_time: datetime):

        self._open_database()
        self.cursor.execute("UPDATE Photos SET PhotoDateTime=? WHERE PhotoID=?", (date_time, entry_id))
        self._close_database()

    def add_location(self, entry_id: int, latitude: float, longitude: float):

        self._open_database()
        self.cursor.execute("UPDATE Photos SET LocationLatitude=?, LocationLongitude=? WHERE PhotoID=?",
                            (latitude, longitude, entry_id))
        self._close_database()

    def add_weather(self, entry_id: int, weather: int):

        self._open_database()
        self.cursor.execute("UPDATE Photos SET Weather=? WHERE PhotoID=?", (weather, entry_id))
        self._close_database()

    def add_color(self, entry_id: int, red_value: float, green_value: float, blue_value: float, color_percentage: int):

        self._open_database()
        self.cursor.execute(
            "INSERT INTO Colors (PhotoID, ColorRed, ColorGreen, ColorBlue, ColorPercentage) VALUES (?, ?, ?, ?, ?)",
            (entry_id, red_value, green_value, blue_value, color_percentage))
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

    def get_entry_id_by_parameters(self, hour_interval_left: str, hour_interval_right: str,
                                   month_interval_left: str, month_interval_right: str,
                                   latitude_interval_left: float, latitude_interval_right: float,
                                   longitude_interval_left: float, longitude_interval_right: float,
                                   weather_interval_left: int, weather_interval_right: int):

        request_text = "SELECT PhotoID FROM Photos WHERE TRUE"

        if (hour_interval_left > hour_interval_right):
            request_text += " AND ((cast(strftime('%H', time(PhotoDateTime)) as INTEGER) >= {}) OR (cast(strftime('%H', time(PhotoDateTime)) as INTEGER) <= {}))".format(
                hour_interval_left, hour_interval_right)
        else:
            request_text += " AND (cast(strftime('%H', time(PhotoDateTime)) as INTEGER) BETWEEN {} AND {})".format(
                hour_interval_left, hour_interval_right)

        if (month_interval_left > month_interval_right):
            request_text += " AND ((cast(strftime('%m', date(PhotoDateTime)) as INTEGER) >= {}) OR (cast(strftime('%m', date(PhotoDateTime)) as INTEGER) <= {}))".format(
                month_interval_left, month_interval_right)
        else:
            request_text += " AND (cast(strftime('%m', date(PhotoDateTime)) as INTEGER) BETWEEN {} AND {})".format(
                month_interval_left, month_interval_right)

        request_text += " AND (LocationLatitude BETWEEN {} AND {})".format(latitude_interval_left,
                                                                           latitude_interval_right)
        request_text += " AND (LocationLongitude BETWEEN {} AND {})".format(longitude_interval_left,
                                                                            longitude_interval_right)
        request_text += " AND (Weather BETWEEN {} AND {})".format(weather_interval_left, weather_interval_right)

        print(request_text)

        self._open_database()
        result = self.cursor.execute(request_text)
        result = result.fetchall()
        self._close_database()

        result_list = []
        for row in result:
            result_list.append(row[0])

        return result_list

    def get_image_name_by_entry_id(self, entry_id: int):

        self._open_database()
        result = self.cursor.execute("SELECT PhotoName FROM Photos WHERE PhotoID=?", (entry_id,))
        result = result.fetchall()
        self._close_database()

        for row in result:
            return row[0]

    def get_location_by_entry_id(self, entry_id: int) -> Tuple[float, float]:

        self._open_database()
        result = self.cursor.execute("SELECT LocationLatitude, LocationLongitude FROM Photos WHERE PhotoID=?",
                                     (entry_id,))
        result = result.fetchall()
        self._close_database()

        for row in result:
            return row[0], row[1]

    def get_datetime_by_entry_id(self, entry_id: int) -> datetime:

        self._open_database()
        result = self.cursor.execute("SELECT datetime(PhotoDateTime) FROM Photos WHERE PhotoID=?",
                                     (entry_id,))
        result = result.fetchall()
        self._close_database()

        for row in result:
            return datetime.fromisoformat(row[0])

    def get_colors_by_entry_id(self, entry_id: int):

        self._open_database()
        result = self.cursor.execute(
            "SELECT ColorRed, ColorGreen, ColorBlue, ColorPercentage FROM Colors WHERE PhotoID=?", (entry_id,))
        result = result.fetchall()
        self._close_database()

        for row in result:
            return row[0], row[1], row[2], row[3]

    def delete_image_by(self, entry_id: int):
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
