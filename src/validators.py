from datetime import date
from decimal import Decimal, InvalidOperation

VALID_TYPES = {"Deposit", "Withdrawal"}
VALID_ACCOUNT_TYPES = {"Savings", "Current", "Student"}

def validate_display_name(name):
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Display name is required.")
    if len(name.strip()) > 100:
        raise ValueError("Display name must be 100 characters or fewer.")
    return name.strip()

def validate_account_type(account_type):
    if account_type not in VALID_ACCOUNT_TYPES:
        raise ValueError("Invalid account type.")
    return account_type

def validate_amount(amount):
    try:
        value = Decimal(str(amount))
    except (InvalidOperation, ValueError, TypeError):
        raise ValueError("Amount must be a valid number.")
    if not value.is_finite() or value <= 0:
        raise ValueError("Amount must be greater than zero.")
    if value.as_tuple().exponent < -2:
        raise ValueError("Amount may have at most two decimal places.")
    return value.quantize(Decimal("0.01"))

def validate_transaction_type(transaction_type):
    if transaction_type not in VALID_TYPES:
        raise ValueError("Transaction type must be Deposit or Withdrawal.")
    return transaction_type

def validate_transaction_date(transaction_date):
    if isinstance(transaction_date, str):
        try:
            transaction_date = date.fromisoformat(transaction_date)
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format.")
    if not isinstance(transaction_date, date):
        raise ValueError("A valid transaction date is required.")
    return transaction_date
