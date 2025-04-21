### PROJECT
### db_operations.py
###  NAME  : DANIEL OLANIYANU
###  CLASS : ADEV-3005 (261248)
###  DATE  : 2025-04-10

from dbcm import DBCM

DB_NAME = "weather.sqlite"

class DBOperations:


    def initialize_db():

        # Create Weather Table using context manager derived cursor
        with DBCM(DB_NAME) as cursor:
            cursor.execute("""CREATE TABLE IF NOT EXISTS weather 
                                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                 date TEXT NOT NULL,
                                 location TEXT NOT NULL,
                                 min_temp REAL,
                                 max_temp REAL,
                                 avg_temp REAL);
                           """)


