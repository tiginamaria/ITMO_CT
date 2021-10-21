# This file contains functions for database management

# Importing required modules
import sqlite3
from datetime import datetime


# Describing class for database operations
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

    def add_color(self, entry_id: int, red_value: float, green_value: float, blue_value: float):
        self._open_database()
        self.cursor.execute("INSERT INTO Colors (PhotoID, ColorRed, ColorGreen, ColorBlue) VALUES (?, ?, ?, ?)",
                            (entry_id, red_value, green_value, blue_value))
        self._close_database()

    # Response functions

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

    def get_entry_id_by_parameters(self, datetime_min: datetime, datetime_max: datetime,
                                   latitude_min: float, latitude_max: float,
                                   longitude_min: float, longitude_max: float,
                                   weather_min: int, weather_max: int):
        self._open_database()
        result = self.cursor.execute(
            "SELECT PhotoID FROM Photos WHERE (datetime(PhotoDateTime) BETWEEN datetime(?) AND datetime(?)) AND (LocationLatitude BETWEEN ? AND ?) AND (LocationLongitude BETWEEN ? AND ?) AND (Weather BETWEEN ? AND ?)",
            (datetime_min, datetime_max, latitude_min, latitude_max, longitude_min, longitude_max, weather_min,
             weather_max))
        result = result.fetchall()
        self._close_database()
        return result

    def get_colors_by_entry_id(self, entry_id: int):
        self._open_database()
        result = self.cursor.execute("SELECT ColorRed, ColorGreen, ColorBlue FROM Colors WHERE PhotoID=?", (entry_id,))
        result = result.fetchall()
        self._close_database()
        return result

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
