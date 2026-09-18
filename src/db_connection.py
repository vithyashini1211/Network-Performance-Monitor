import os

import mysql.connector
from dotenv import load_dotenv


# Load variables from the .env file
load_dotenv()


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )


if __name__ == "__main__":
    try:
        connection = get_connection()

        if connection.is_connected():
            print("SUCCESS: Python connected to MySQL!")
            print(f"Database: {os.getenv('DB_NAME')}")

        connection.close()

    except mysql.connector.Error as error:
        print("ERROR: Could not connect to MySQL")
        print(error)