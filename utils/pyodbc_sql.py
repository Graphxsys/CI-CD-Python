"""
MSSQL Database Utility

This script provides a class for interacting with an MSSQL database. It includes
methods to execute queries, retrieve column names, delete table data, and insert CSV data.

Modules Used:
- os: For environment variable handling.
- pyodbc: For connecting to and interacting with an MSSQL database.
- dotenv: For loading environment variables from a .env file.
"""

import os
import pyodbc

class MSSQLDatabase:
    """
    A class for executing SQL queries and performing data operations with an MSSQL database.

    Attributes:
        server (str): The name of the SQL server.
        database (str): The name of the database.
        username (str): The username for the SQL server.
        password (str): The password for the SQL server.
        conn (pyodbc.Connection): The connection to the SQL server.
    """

    def __init__(self):
        """
        Initializes the MSSQLDatabase class by retrieving database credentials from environment variables.
        """
        self.server = os.getenv("SQL_SERVER")
        self.database = os.getenv("SQL_DATABASE")
        self.username = os.getenv("SQL_USERNAME")
        self.password = os.getenv("SQL_PASSWORD")
        self.conn = None

    def execute_query(self, query: str) -> list[tuple[str, str]]:
        """
        Executes a SQL query and returns the result if applicable.

        Args:
            query (str): The SQL query to execute.
        
        Returns:
            list[tuple[str, str]] | None: The result of the query, or None if an error occurs.
        """
        try:
            conn = pyodbc.connect(
                f"""DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={self.server};DATABASE={self.database};
                    UID={self.username};PWD={self.password}""",
                TrustServerCertificate="yes",
            )
            cursor = conn.cursor()
            cursor.execute(query)

            if cursor.description is not None:
                data = cursor.fetchall()
            else:
                data = None

            conn.commit()
            cursor.close()
            conn.close()
            return data
        except Exception as e:
            print(f"Exception occurred: {type(e).__name__} - {e}")
            return None

if __name__ == "__main__":
    import os
    from dotenv import load_dotenv

    load_dotenv()

    sql = MSSQLDatabase()
    
    # Execute a query to retrieve active user data
    result = sql.execute_query("SELECT 'Test' AS Result")
    print(result)  # Output: [('Test',)]
