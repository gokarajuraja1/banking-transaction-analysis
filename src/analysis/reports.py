import numpy as np
import pandas as pd

def transaction_statistics(transactions):
    if transactions.empty:
        return {"total_deposits": 0.0, "total_withdrawals": 0.0, "average_amount": 0.0,
                "median_amount": 0.0, "transaction_count": 0}
    amounts = pd.to_numeric(transactions["amount"], errors="coerce").dropna().to_numpy(dtype=float)
    deposits = transactions.loc[transactions["transaction_type"] == "Deposit", "amount"].astype(float).sum()
    withdrawals = transactions.loc[transactions["transaction_type"] == "Withdrawal", "amount"].astype(float).sum()
    return {
        "total_deposits": float(deposits),
        "total_withdrawals": float(withdrawals),
        "average_amount": float(np.mean(amounts)) if len(amounts) else 0.0,
        "median_amount": float(np.median(amounts)) if len(amounts) else 0.0,
        "transaction_count": int(len(transactions)),
    }

def monthly_summary(transactions):
    if transactions.empty:
        return pd.DataFrame(columns=["month", "deposit_total", "withdrawal_total", "transaction_count"])
    frame = transactions.copy()
    frame["transaction_date"] = pd.to_datetime(frame["transaction_date"])
    frame["month"] = frame["transaction_date"].dt.to_period("M").astype(str)
    frame["amount"] = pd.to_numeric(frame["amount"])
    grouped = frame.pivot_table(index="month", columns="transaction_type", values="amount",
                                aggfunc="sum", fill_value=0)
    for kind in ("Deposit", "Withdrawal"):
        if kind not in grouped.columns:
            grouped[kind] = 0.0
    counts = frame.groupby("month").size().rename("transaction_count")
    result = grouped.rename(columns={"Deposit": "deposit_total", "Withdrawal": "withdrawal_total"})
    result = result[["deposit_total", "withdrawal_total"]].join(counts)
    return result.reset_index().sort_values("month")

def transaction_type_summary(transactions):
    if transactions.empty:
        return pd.DataFrame(columns=["transaction_type", "count", "total_amount", "average_amount"])
    frame = transactions.copy()
    frame["amount"] = pd.to_numeric(frame["amount"])
    return frame.groupby("transaction_type", as_index=False).agg(
        count=("transaction_id", "count"), total_amount=("amount", "sum"), average_amount=("amount", "mean")
    )
