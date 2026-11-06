import pandas as pd
from src.db import cursor_context
from src.validators import validate_display_name

def create_customer(display_name):
    name = validate_display_name(display_name)
    with cursor_context() as (_, cursor):
        cursor.execute("INSERT INTO customers (display_name) VALUES (%s)", (name,))
        return cursor.lastrowid

def list_customers():
    with cursor_context() as (_, cursor):
        cursor.execute("SELECT customer_id, display_name, created_at FROM customers ORDER BY customer_id DESC")
        rows = cursor.fetchall()
    return pd.DataFrame(rows, columns=["customer_id", "display_name", "created_at"])
