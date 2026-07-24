import os

import psycopg2


def obtener_conexion():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "iadb"),
        user=os.getenv("DB_USER", "app_ia"),
        password=os.getenv("DB_PASSWORD", "clave_app_ia"),
    )
