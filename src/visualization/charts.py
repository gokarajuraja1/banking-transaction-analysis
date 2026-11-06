

import pandas as pd
import matplotlib.pyplot as plt


def transaction_type_chart(transactions):
    # Smaller graph: width=4, height=2.5 inches
    fig, ax = plt.subplots(figsize=(4, 2.5))

    if (
        transactions is None
        or transactions.empty
        or "transaction_type" not in transactions.columns
        or "amount" not in transactions.columns
    ):
        ax.text(
            0.5, 0.5,
            "No transactions yet",
            ha="center",
            va="center"
        )
        ax.set_axis_off()
        fig.tight_layout()
        return fig

    data = transactions.copy()
    data["amount"] = pd.to_numeric(
        data["amount"], errors="coerce"
    )
    data = data.dropna(
        subset=["transaction_type", "amount"]
    )

    if data.empty:
        ax.text(
            0.5, 0.5,
            "No valid transaction data",
            ha="center",
            va="center"
        )
        ax.set_axis_off()
        fig.tight_layout()
        return fig

    totals = (
        data.groupby("transaction_type")["amount"]
        .sum()
        .reindex(["Deposit", "Withdrawal"], fill_value=0)
    )

    totals.plot(kind="bar", ax=ax)
    ax.set_title("Deposits vs Withdrawals", fontsize=10)
    ax.set_xlabel("Transaction type", fontsize=8)
    ax.set_ylabel("Amount (₹)", fontsize=8)
    ax.tick_params(axis="x", rotation=0, labelsize=8)
    ax.tick_params(axis="y", labelsize=8)
    fig.tight_layout()
    return fig


def monthly_trend_chart(monthly):
    # Smaller graph: width=5, height=2.5 inches
    fig, ax = plt.subplots(figsize=(5, 2.5))

    if (
        monthly is not None
        and not monthly.empty
        and {"month", "deposit_total", "withdrawal_total"}
        .issubset(monthly.columns)
    ):
        ax.plot(
            monthly["month"],
            monthly["deposit_total"],
            marker="o",
            markersize=3,
            linewidth=1.2,
            label="Deposits"
        )
        ax.plot(
            monthly["month"],
            monthly["withdrawal_total"],
            marker="o",
            markersize=3,
            linewidth=1.2,
            label="Withdrawals"
        )
        ax.legend(fontsize=8)
    else:
        ax.text(
            0.5, 0.5,
            "No monthly data available",
            ha="center",
            va="center"
        )

    ax.set_title("Monthly Transaction Trend", fontsize=10)
    ax.set_xlabel("Month", fontsize=8)
    ax.set_ylabel("Amount (₹)", fontsize=8)
    ax.tick_params(axis="x", rotation=45, labelsize=8)
    ax.tick_params(axis="y", labelsize=8)
    fig.tight_layout()
    return fig
