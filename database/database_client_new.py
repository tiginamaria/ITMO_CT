# This file contains functions for database management

# Importing required modules
import sqlite3
from datetime import datetime

# Describing class for database operations
class ImageDatabase:
    
    def __init__(self, database_path):
        # Add reading database path from config file
        self.db_path = database_path
     
    def add_new_photo(self, photo_name):
        current_dt = datetime.utcnow()
        current_dt = str(current_dt).split('.')[0]
        self._open_database()
        self.cursor.execute("INSERT INTO Photos (PhotoName, UploadDateTime) VALUES (?, ?)", (photo_name, current_dt))
        self._close_database()
    
    def add_datetime(self, entry_id, date_time):
        self._open_database()
        self.cursor.execute("UPDATE Photos SET PhotoDateTime = ? WHERE PhotoID = ?", (date_time, entry_id))
        self._close_database()
    
    def add_location(self, entry_id, latitude, longitude):
        self._open_database()
        self.cursor.execute("UPDATE Photos SET LocationLatitude = ?, LocationLongitude = ? WHERE PhotoID = ?", (latitude, longitude, entry_id))
        self._close_database()
        
    def add_weather(self, entry_id, weather):
        self._open_database()
        self.cursor.execute("UPDATE Photos SET Weather = ? WHERE PhotoID = ?", (weather, entry_id))
        self._close_database()
        
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
        
    def _get_all_entries(self):
        self._open_database()
        self.cursor.execute("SELECT * FROM Photos")
        entries = self.cursor.fetchall()
        self._close_database()
        return entries
        