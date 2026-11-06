import pytest
from datetime import date
from decimal import Decimal
from src.validators import (validate_amount, validate_transaction_type, validate_display_name,
                            validate_transaction_date, validate_account_type)

def test_valid_amount():
    assert validate_amount("12.50") == Decimal("12.50")

@pytest.mark.parametrize("amount", [0, -1, "abc", None, "1.999"])
def test_invalid_amount(amount):
    with pytest.raises(ValueError):
        validate_amount(amount)

def test_valid_transaction_type():
    assert validate_transaction_type("Deposit") == "Deposit"

def test_invalid_transaction_type():
    with pytest.raises(ValueError):
        validate_transaction_type("Transfer")

def test_display_name_trimmed():
    assert validate_display_name("  Sample  ") == "Sample"

def test_blank_display_name_rejected():
    with pytest.raises(ValueError):
        validate_display_name("  ")

def test_date():
    assert validate_transaction_date("2026-01-05") == date(2026, 1, 5)

def test_invalid_account_type():
    with pytest.raises(ValueError):
        validate_account_type("Premium")
