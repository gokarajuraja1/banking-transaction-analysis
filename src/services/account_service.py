import pandas as pd
from src.db import cursor_context
from src.validators import validate_account_type

def create_account(customer_id, account_type, opening_balance=0):
    kind = validate_account_type(account_type)
    try:
        balance = float(opening_balance)
    except (TypeError, ValueError):
        raise ValueError("Opening balance must be a number.")
    if balance < 0:
        raise ValueError("Opening balance cannot be negative.")
    with cursor_context() as (_, cursor):
        cursor.execute("SELECT customer_id FROM customers WHERE customer_id = %s", (int(customer_id),))
        if cursor.fetchone() is None:
            raise ValueError("Customer does not exist.")
        cursor.execute(
            "INSERT INTO accounts (customer_id, account_type, opening_balance) VALUES (%s, %s, %s)",
            (int(customer_id), kind, round(balance, 2)),
        )
        return cursor.lastrowid

def list_accounts():
    query = """
        SELECT a.account_id, a.customer_id, c.display_name, a.account_type,
               a.opening_balance,
               a.opening_balance + COALESCE(SUM(CASE
                   WHEN t.transaction_type = 'Deposit' THEN t.amount
                   ELSE -t.amount END), 0) AS simulated_balance,
               a.created_at
        FROM accounts a
        JOIN customers c ON c.customer_id = a.customer_id
        LEFT JOIN transactions t ON t.account_id = a.account_id
        GROUP BY a.account_id, a.customer_id, c.display_name, a.account_type,
                 a.opening_balance, a.created_at
        ORDER BY a.account_id DESC
    """
    with cursor_context() as (_, cursor):
        cursor.execute(query)
        rows = cursor.fetchall()
    return pd.DataFrame(rows, columns=["account_id", "customer_id", "display_name", "account_type",
                                       "opening_balance", "simulated_balance", "created_at"])

def get_account_summary(account_id):
    query = """
        SELECT a.account_id, c.display_name, a.account_type, a.opening_balance,
          COALESCE(SUM(CASE WHEN t.transaction_type='Deposit' THEN t.amount ELSE 0 END),0) AS total_deposits,
          COALESCE(SUM(CASE WHEN t.transaction_type='Withdrawal' THEN t.amount ELSE 0 END),0) AS total_withdrawals,
          a.opening_balance + COALESCE(SUM(CASE WHEN t.transaction_type='Deposit' THEN t.amount
                                                ELSE -t.amount END),0) AS simulated_balance,
          COUNT(t.transaction_id) AS transaction_count
        FROM accounts a JOIN customers c ON c.customer_id=a.customer_id
        LEFT JOIN transactions t ON t.account_id=a.account_id
        WHERE a.account_id=%s
        GROUP BY a.account_id, c.display_name, a.account_type, a.opening_balance
    """
    with cursor_context() as (_, cursor):
        cursor.execute(query, (int(account_id),))
        rows = cursor.fetchall()
    return pd.DataFrame(rows)
