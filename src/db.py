import os
from contextlib import contextmanager
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        database=os.getenv("DB_NAME", "banking_analysis"),
        user=os.getenv("DB_USER", "banking_app"),
        password=os.getenv("DB_PASSWORD", ""),
        connection_timeout=5,
    )

@contextmanager
def cursor_context(dictionary=True):
    connection = get_connection()
    cursor = connection.cursor(dictionary=dictionary)
    try:
        yield connection, cursor
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()
