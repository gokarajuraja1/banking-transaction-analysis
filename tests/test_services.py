import pandas as pd
from src.analysis.reports import transaction_statistics, monthly_summary, transaction_type_summary

def sample_transactions():
    return pd.DataFrame([
        {"transaction_id": 1, "transaction_date": "2026-01-05", "transaction_type": "Deposit", "amount": 1000.0},
        {"transaction_id": 2, "transaction_date": "2026-01-08", "transaction_type": "Withdrawal", "amount": 200.0},
        {"transaction_id": 3, "transaction_date": "2026-02-01", "transaction_type": "Deposit", "amount": 500.0},
    ])

def test_statistics():
    result = transaction_statistics(sample_transactions())
    assert result["total_deposits"] == 1500.0
    assert result["total_withdrawals"] == 200.0
    assert result["transaction_count"] == 3

def test_monthly_summary():
    result = monthly_summary(sample_transactions())
    assert len(result) == 2
    assert result.loc[result["month"] == "2026-01", "deposit_total"].iloc[0] == 1000.0

def test_transaction_type_summary():
    result = transaction_type_summary(sample_transactions())
    assert set(result["transaction_type"]) == {"Deposit", "Withdrawal"}

def test_empty_statistics():
    empty = pd.DataFrame(columns=["transaction_id", "transaction_date", "transaction_type", "amount"])
    assert transaction_statistics(empty)["transaction_count"] == 0
