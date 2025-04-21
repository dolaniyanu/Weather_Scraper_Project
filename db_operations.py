### PROJECT
### db_operations.py
###  NAME  : DANIEL OLANIYANU
###  CLASS : ADEV-3005 (261248)
###  DATE  : 2025-04-10

from dbcm import DBCM
from weather_scraper import WeatherScraper

DB_NAME = "weather.sqlite"

class DBOperations:


    def initialize_db():

        # Create Weather Table using context manager derived cursor
        with DBCM(DB_NAME) as cursor:
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
    
    def save_data(data_dict, location="Winnipeg, MB"):

        sqltable_insert = """INSERT OR IGNORE INTO weather
                            (sample_date,location,min_temp,max_temp,avg_temp)
                            VALUES (?,?,?,?,?);"""
        

        # Store Weather Table data using context manager derived cursor
        with DBCM(DB_NAME) as cursor:
            for month, daily_data in data_dict.items(): # Stores data in dictionary of tuples
                for day, max_temp, min_temp, avg_temp in daily_data:
                    date_str = f"{month}-{day:02d}"
                    data = (date_str, location, min_temp, max_temp, avg_temp)
                    cursor.execute(sqltable_insert, data)

    def fetch_data():

        # Fetch all Weather Table data using context manager derived cursor
        with DBCM(DB_NAME) as cursor:
            cursor.execute("""SELECT sample_date,location,min_temp,max_temp,avg_temp
                              FROM weather
                              ORDER BY sample_date DESC;
                           """)
            return cursor.fetchall()
        
    def purge_data():

        with DBCM(DB_NAME) as cursor:
            cursor.execute("DELETE FROM weather;")


