import os
import pandas as pd
from dotenv import load_dotenv
from src.db import cursor_context
from src.validators import validate_amount, validate_transaction_type, validate_transaction_date

load_dotenv()

def record_transaction(account_id, transaction_type, amount, transaction_date, description=""):
    kind = validate_transaction_type(transaction_type)
    value = validate_amount(amount)
    tx_date = validate_transaction_date(transaction_date)
    note = (description or "").strip()[:200] or None
    with cursor_context() as (_, cursor):
        cursor.execute("SELECT account_id, opening_balance FROM accounts WHERE account_id=%s FOR UPDATE",
                       (int(account_id),))
        account = cursor.fetchone()
        if account is None:
            raise ValueError("Account does not exist.")
        if kind == "Withdrawal":
            cursor.execute("""
                SELECT COALESCE(SUM(CASE WHEN transaction_type='Deposit' THEN amount ELSE -amount END), 0) AS net
                FROM transactions WHERE account_id=%s
            """, (int(account_id),))
            net = cursor.fetchone()["net"] or 0
            balance = float(account["opening_balance"]) + float(net)
            if float(value) > balance:
                raise ValueError("Insufficient simulated balance for this withdrawal.")
        cursor.execute("""
            INSERT INTO transactions (account_id, transaction_date, transaction_type, amount, description)
            VALUES (%s, %s, %s, %s, %s)
        """, (int(account_id), tx_date, kind, float(value), note))
        return cursor.lastrowid

def list_transactions():
    query = """
        SELECT t.transaction_id, t.account_id, c.display_name, t.transaction_date,
               t.transaction_type, t.amount, t.description, t.created_at
        FROM transactions t
        JOIN accounts a ON a.account_id=t.account_id
        JOIN customers c ON c.customer_id=a.customer_id
        ORDER BY t.transaction_date DESC, t.transaction_id DESC
    """
    with cursor_context() as (_, cursor):
        cursor.execute(query)
        rows = cursor.fetchall()
    return pd.DataFrame(rows, columns=["transaction_id", "account_id", "display_name",
                                       "transaction_date", "transaction_type", "amount",
                                       "description", "created_at"])

def review_flags():
    threshold = float(os.getenv("REVIEW_AMOUNT_THRESHOLD", "50000"))
    query = """
        SELECT t.transaction_id, t.account_id, c.display_name, t.transaction_date,
               t.transaction_type, t.amount, t.description,
               'Amount meets or exceeds review threshold' AS review_reason
        FROM transactions t
        JOIN accounts a ON a.account_id=t.account_id
        JOIN customers c ON c.customer_id=a.customer_id
        WHERE t.amount >= %s
        ORDER BY t.transaction_date DESC
    """
    with cursor_context() as (_, cursor):
        cursor.execute(query, (threshold,))
        rows = cursor.fetchall()
    return pd.DataFrame(rows)
