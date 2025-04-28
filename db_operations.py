### PROJECT
### db_operations.py
###  NAME  : DANIEL OLANIYANU
###  CLASS : ADEV-3005 (261248)
###  DATE  : 2025-04-10

"""
db_operations.py

Manages database operations related to weather data storage, retrieval, and deletion.
"""

import logging
from dbcm import DBCM

# Configure logging
logging.basicConfig(
    filename='weather_app.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

DB_NAME = "weather.sqlite"

class DBOperations:
    """
    This class manages the database SQL operations for the weather database.
    """

    @staticmethod
    def initialize_db():
        """
        Creates the weather table if it does not already exist.
        """
        try:
            with DBCM(DB_NAME) as cursor:
                # Create the weather table using the context manager derived cursor
                cursor.execute("""CREATE TABLE IF NOT EXISTS weather 
                                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                sample_date TEXT NOT NULL,
                                location TEXT NOT NULL,
                                min_temp REAL,
                                max_temp REAL,
                                avg_temp REAL,
                                UNIQUE(sample_date, location));
                            """)
        except Exception as e:
            logging.error('Error in initialize_db: %s', e)
            raise

    @staticmethod
    def save_data(data_dict, location="Winnipeg, MB"):
        """
        Inserts scraped weather data into the database.

        Args:
            data_dict (dict): Dictionary with month as key and list of (day, max, min, mean) tuples.
            location (str): Location name, defaults to "Winnipeg, MB".
        """
        try:
            sql_insert = """INSERT OR IGNORE INTO weather
                            (sample_date, location, min_temp, max_temp, avg_temp)
                            VALUES (?, ?, ?, ?, ?);"""
            with DBCM(DB_NAME) as cursor:
                # Store weather data from the dictionary
                for month, daily_data in data_dict.items():
                    for day, max_temp, min_temp, avg_temp in daily_data:
                        date_str = f"{month}-{day:02d}"
                        data = (date_str, location, min_temp, max_temp, avg_temp)
                        cursor.execute(sql_insert, data)
        except Exception as e:
            logging.error('Error in save_data: %s', e)
            raise

    @staticmethod
    def fetch_data():
        """
        Retrieves all stored weather data from the database.

        Returns:
            list: List of tuples containing weather data records.
        """
        try:
            with DBCM(DB_NAME) as cursor:
                # Fetch all weather table data
                cursor.execute("""SELECT sample_date, location, min_temp, max_temp, avg_temp
                                  FROM weather
                                  ORDER BY sample_date DESC;""")
                return cursor.fetchall()
        except Exception as e:
            logging.error('Error in fetch_data: %s', e)
            raise

    @staticmethod
    def purge_data():
        """
        Deletes all weather data from the database.
        """
        try:
            with DBCM(DB_NAME) as cursor:
                # Delete all weather table data
                cursor.execute("DELETE FROM weather;")
        except Exception as e:
            logging.error('Error in purge_data: %s', e)
            raise
