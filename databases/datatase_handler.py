import sqlite3
import os


class Database(object):
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
        except sqlite3.Error as e:
            print("Error connecting to database:", e)

    def execute_query(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            #print("Query executed successfully")
        except sqlite3.Error as e:
            print("Error executing query:", e)

    def fetch_data(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)

            rows = self.cursor.fetchall()
            return rows
        except sqlite3.Error as e:
            print("Error fetching data:", e)

    def delete_data(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
            #print("Data deleted successfully")
        except sqlite3.Error as e:
            print("Error deleting data:", e)

    def close(self):
        try:
            if self.connection:
                self.connection.close()
                #print("Database connection closed")
        except sqlite3.Error as e:
            print("Error closing database connection:", e)

    def is_table_empty(self, table_name):
        try:
            query = "SELECT COUNT(*) FROM {}".format(table_name)
            result = self.fetch_data(query)
            if result:
                count = result[0][0]
                return count == 0
            else:
                print("Failed to fetch count of rows.")
                return False
        except sqlite3.Error as e:
            print("Error checking if table is empty:", e)
            return False


class DatabaseWorkflowProductUserConnection(Database):

    def __init__(self, db_name):

        super().__init__(db_name)
        self.db_name = db_name
        self.main_dir = os.path.dirname(os.path.abspath(__file__))
        self.database_dir = None

    def create_db_if_not_exists(self):
        self.database_dir = os.path.join(self.main_dir, self.db_name)
        if not os.path.exists(self.database_dir):
            conn = sqlite3.connect(self.database_dir)
            conn.close()









