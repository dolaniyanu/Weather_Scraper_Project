### PROJECT
### db_operations.py
###  NAME  : DANIEL OLANIYANU
###  CLASS : ADEV-3005 (261248)
###  DATE  : 2025-04-10

from dbcm import DBCM
import logging
from weather_scraper import WeatherScraper

DB_NAME = "weather.sqlite"

class DBOperations:
    """
    This class manages the database SQL code for weather db.
    """

    def initialize_db():
        """
        Creates the weather table if it doesn't exist.
        """
        try:
            with DBCM(DB_NAME) as cursor:
            # Create Weather Table using context manager derived cursor
                cursor.execute("""CREATE TABLE IF NOT EXISTS weather 
                                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    sample_date TEXT NOT NULL,
                                    location TEXT NOT NULL,
                                    min_temp REAL,
                                    max_temp REAL,
                                    avg_temp REAL,
                                    UNIQUE(sample_date, location)
                                    );
                            """)
        except Exception as e:
            logging.error(f'Error in initialize_db: {e}')
            raise
    
    def save_data(data_dict, location="Winnipeg, MB"):
        """
        Inserts scraped weather data into the database.

        Args:
            data_dict (dict): Dictionary with month as key and list of (day, max, min, mean) tuples.
            location (str): Location name, defaults to "Winnipeg, MB".
        """
        try:
            sqltable_insert = """INSERT OR IGNORE INTO weather
                                (sample_date,location,min_temp,max_temp,avg_temp)
                                VALUES (?,?,?,?,?);"""
            with DBCM(DB_NAME) as cursor:
            # Store Weather Table data using context manager derived cursor
                for month, daily_data in data_dict.items(): # Stores data in dictionary of tuples
                    for day, max_temp, min_temp, avg_temp in daily_data:
                        date_str = f"{month}-{day:02d}"
                        data = (date_str, location, min_temp, max_temp, avg_temp)
                        cursor.execute(sqltable_insert, data)
        except Exception as e:
            logging.error(f'Error in save_data: {e}')
            raise

    def fetch_data():
        """
        Retrieves all stored weather data.

        Returns:
            list: List of tuples with weather data records.
        """
        try:
            with DBCM(DB_NAME) as cursor:
            # Fetch all Weather Table data using context manager derived cursor
                cursor.execute("""SELECT sample_date,location,min_temp,max_temp,avg_temp
                                FROM weather
                                ORDER BY sample_date DESC;
                            """)
                return cursor.fetchall()
        except Exception as e:
            logging.error(f'Error in fetch_data: {e}')
            raise
        
    def purge_data():
        """
        Deletes all weather data from the table.
        """
        try:
            with DBCM(DB_NAME) as cursor:
            # Delete all Weather Table data using context manager derived cursor
                cursor.execute("DELETE FROM weather;")
        except Exception as e:
            logging.error(f'Error in purge_data: {e}')
            raise

# Logging
logging.basicConfig(
    filename='weather_app.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)