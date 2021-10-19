# This file contains functions for database management

# Importing required modules
import sqlite3
from datetime import datetime

# Describing class for database operations
class ImageDatabase:
    
    def __init__(self, database_path):
        self.db_path = database_path
     
    def add_new_photo(self, photo_name):
        current_dt = datetime.utcnow()
        current_dt = str(current_dt).split('.')[0]
        self._open_database()
        result = self.cursor.execute("INSERT INTO Photos (PhotoName, UploadDateTime) VALUES (?, ?)", (photo_name, current_dt))
        entry_id = result.lastrowid
        self._close_database()
        return entry_id
    
    def add_datetime(self, entry_id, date_time):
        self._open_database()
        self.cursor.execute("UPDATE Photos SET PhotoDateTime=? WHERE PhotoID=?", (date_time, entry_id))
        self._close_database()
    
    def add_location(self, entry_id, latitude, longitude):
        self._open_database()
        self.cursor.execute("UPDATE Photos SET LocationLatitude=?, LocationLongitude=? WHERE PhotoID=?", (latitude, longitude, entry_id))
        self._close_database()
        
    def add_weather(self, entry_id, weather):
        self._open_database()
        self.cursor.execute("UPDATE Photos SET Weather=? WHERE PhotoID=?", (weather, entry_id))
        self._close_database()
        
    def add_color(self, entry_id, red_value, green_value, blue_value):
        self._open_database()
        self.cursor.execute("INSERT INTO Colors (PhotoID, ColorRed, ColorGreen, ColorBlue) VALUES (?, ?, ?, ?)", (entry_id, red_value, green_value, blue_value))
        self._close_database()
        
    def get_image_name_by_exact_color(self, red_value, green_value, blue_value):
        self._open_database()
        result = self.cursor.execute("SELECT PhotoName FROM Photos WHERE PhotoID IN (SELECT PhotoID FROM Colors WHERE ColorRed=? AND ColorGreen=? AND ColorBlue=?)", (red_value, green_value, blue_value))
        result = result.fetchall()
        self._close_database()
        return result
    
    def get_color_by_parameters(self, month_min, month_max, latitude_min, latitude_max, longitude_min, longitude_max, weather_min, weather_max):
        # To implement
        return False
        
    def _open_database(self):
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        
    def _close_database(self):
        self.connection.commit()
        self.connection.close()
        
    def _delete_entry(self, entry_id):
        self._open_database()
        self.cursor.execute("DELETE FROM Photos WHERE PhotoID=?", (entry_id,))
        self._close_database()
        
    def _get_all_entries(self, table_name):
        self._open_database()
        self.cursor.execute("SELECT * FROM {}".format(table_name))
        entries = self.cursor.fetchall()
        self._close_database()
        return entries
        