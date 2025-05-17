import mysql.connector
from mysql.connector import Error
import pandas as pd
import os
from dotenv import load_dotenv

# Tải biến môi trường từ file .env
load_dotenv()

class Connect:
    @staticmethod
    def connect_db():
        try:
            connection = mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASS"),
                database=os.getenv("DB_NAME")
            )
            if connection.is_connected():
                print("Connected to MySQL database")
                return connection
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None

    @staticmethod
    def fetch_data(query):
        connection = Connect.connect_db()
        if connection:
            try:
                # Sử dụng pandas để đọc dữ liệu từ truy vấn SQL
                df = pd.read_sql(query, connection)
                return df
            except Error as e:
                print(f"Error executing query: {e}")
                return None
            finally:
                connection.close()
                print("MySQL connection closed")
        return None
