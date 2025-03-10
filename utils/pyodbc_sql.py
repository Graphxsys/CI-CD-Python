import os
import pyodbc
from dotenv import load_dotenv

load_dotenv()

class MSSQLDatabase:
    """
    A class for executing SQL queries and performing data operations with a SQL database.

    :Attributes:
        server: The name of the SQL server.
        database: The name of the database.
        username: The username for the SQL server.
        password: The password for the SQL server.
        conn: The connection to the SQL server.

    :Methods:
        :execute_query(self, query: str) -> Any: Executes the specified SQL query and returns the result.
        :get_column_names(self, table_name: str) -> list[tuple[str, str]]: Returns the column names of the specified table.
        :delete_table_data(self, table_name: str) -> None: Deletes the data from the specified table.
        :insert_csv_data(self, table_name: str, csv_file_path: str) -> None:
        :bulk_insert_csv_sql(self, file_path: str, staging_table_name: str, client_id: str) -> None:
    """

    def __init__(self):
        """
        Initializes the MSSQLDatabase class.

        :return: None
        :rtype: None
        """
        self.server = os.getenv("SQL_SERVER")
        self.database = os.getenv("SQL_DATABASE")
        self.username = os.getenv("SQL_USERNAME")
        self.password = os.getenv("SQL_PASSWORD")
        self.conn = None

    def execute_query(self, query: str) -> list[tuple[str, str]]:
        """
        Executes a SQL query and returns the result.

        :param query: The SQL query to execute.
        :type query: str

        :return: The result of the query.
        :rtype: list[tuple[str, str]] | None
        """

        try:
            conn = pyodbc.connect(
                f"""DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={self.server};DATABASE={self.database};
                                    UID={self.username};PWD={self.password}""",
                TrustServerCertificate="yes",
            )
            cursor = conn.cursor()
            # print("Obtained a valid connection")
            cursor.execute(query)
            # print("Executed AFC table query")

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
    sql = MSSQLDatabase()

    results = sql.execute_query("SELECT * FROM AFC_Password_Tbl WHERE Active = 1")
    for result in results:
        client_id, _, username, password, __ = result
        # print(result)
        print(f'Client ID: {client_id}, Username: {username}, password = {password}')