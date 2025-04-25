### PROJECT
### dbcm.py
###  NAME  : DANIEL OLANIYANU
###  CLASS : ADEV-3005 (261248)
###  DATE  : 2025-04-20

import sqlite3

class DBCM:
    """
    This class manages the SQLite database connections using context management.
    """
    def  __init__(self, db_name):
        """
        Initializes the DBCM object with a database name.

        Args:
            db_name (str): The SQLite database filename.
        """
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def  __enter__(self):
        """
        Opens a database connection and returns the cursor.

        Returns:
            cursor: SQLite cursor object.
        """
        self.connection = sqlite3.connect(self.db_name) # Establish SQLite database connection.
        self.cursor = self.connection.cursor() # Make connection an extension of cursor definition.
        return self.cursor # Return cursor
    
    def __exit__(self, error_type, error_value, error_tb):
        """
        Closes the database connection, commits if no error, otherwise rolls back.

        Args:
            error_type (type): Exception type.
            error_value (Exception): Exception value.
            error_tb (traceback): Exception traceback.
        """
        if self.connection: # Checks if there is a database connection.
            if error_type is None:
                self.connection.commit() # Saves Inserts if there is no error.
            else:
                self.connection.rollback() # Undo changes if there is an error.
            self.cursor.close() 
            self.connection.close()
