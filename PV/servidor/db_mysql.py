import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # tu contraseña si la tienes
        database="punto_de_venta"
    )
