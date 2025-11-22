# db.py
import mysql.connector
from mysql.connector import Error

# Ajusta estos valores a los tuyos
HOST = "localhost"
PORT = 3306
USER = "root"
PASSWORD = "root"
DATABASE = "vitalia_db"

def get_connection():
    try:
        conn = mysql.connector.connect(
            host=HOST,
            port=PORT,
            user=USER,
            password=PASSWORD,
            database=DATABASE,
            autocommit=True
        )
        return conn
    except Error as e:
        print("Error al conectar a la BD:", e)
        return None
