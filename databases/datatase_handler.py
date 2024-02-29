import sqlite3


class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
            #print(f"Connected to database: {self.db_name}")
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
            #print(f'rows = {rows}')
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
