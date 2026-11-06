import streamlit as st
import pandas as pd
from src.auth import require_access
from src.services.customer_service import create_customer, list_customers
from src.services.account_service import create_account, list_accounts, get_account_summary
from src.services.transaction_service import record_transaction, list_transactions, review_flags
from src.analysis.reports import monthly_summary, transaction_type_summary, transaction_statistics
from src.visualization.charts import transaction_type_chart, monthly_trend_chart

st.set_page_config(page_title="Banking Transaction Analysis", page_icon="🏦", layout="wide")
st.title("🏦 Banking Transaction Analysis System")
st.caption("Educational simulation using synthetic data only. Balances are simulated; this is not a real banking platform.")

require_access()

try:
    customers = list_customers()
    accounts = list_accounts()
except Exception as exc:
    st.error("Could not connect to MySQL. Check that MySQL is running and your .env settings are correct.")
    st.code(str(exc))
    st.stop()

tab_dashboard, tab_customers, tab_accounts, tab_transactions, tab_reports = st.tabs(
    ["Dashboard", "Customers", "Accounts", "Transactions", "Reports"]
)

with tab_dashboard:
    transactions = list_transactions()
    c1, c2, c3 = st.columns(3)
    c1.metric("Customers", len(customers))
    c2.metric("Accounts", len(accounts))
    c3.metric("Transactions", len(transactions))
    if not transactions.empty:
        stats = transaction_statistics(transactions)
        a, b, c = st.columns(3)
        a.metric("Total deposits", f"₹{stats['total_deposits']:,.2f}")
        b.metric("Total withdrawals", f"₹{stats['total_withdrawals']:,.2f}")
        c.metric("Average transaction", f"₹{stats['average_amount']:,.2f}")
        st.pyplot(transaction_type_chart(transactions), clear_figure=True)
        st.pyplot(monthly_trend_chart(monthly_summary(transactions)), clear_figure=True)
    else:
        st.info("No transactions yet. Add synthetic records in the Transactions tab.")

with tab_customers:
    st.subheader("Create a sample customer")
    with st.form("customer_form"):
        display_name = st.text_input("Display name")
        customer_submit = st.form_submit_button("Create customer")
    if customer_submit:
        try:
            cid = create_customer(display_name)
            st.success(f"Customer created. ID: {cid}")
            st.rerun()
        except ValueError as exc:
            st.error(str(exc))
    st.dataframe(customers, use_container_width=True, hide_index=True)

with tab_accounts:
    st.subheader("Create an account")
    if customers.empty:
        st.info("Create a customer first.")
    else:
        customer_options = {f"{row['display_name']} (ID {row['customer_id']})": int(row["customer_id"])
                            for _, row in customers.iterrows()}
        with st.form("account_form"):
            selected_customer = st.selectbox("Customer", list(customer_options.keys()))
            account_type = st.selectbox("Account type", ["Savings", "Current", "Student"])
            opening_balance = st.number_input("Simulated opening balance (₹)", min_value=0.0, value=0.0, step=100.0)
            account_submit = st.form_submit_button("Create account")
        if account_submit:
            try:
                aid = create_account(customer_options[selected_customer], account_type, opening_balance)
                st.success(f"Account created. ID: {aid}")
                st.rerun()
            except (ValueError, RuntimeError) as exc:
                st.error(str(exc))
    st.dataframe(accounts, use_container_width=True, hide_index=True)
    if not accounts.empty:
        account_id = st.selectbox("View account summary", accounts["account_id"].astype(int).tolist(), key="summary_account")
        st.dataframe(get_account_summary(account_id), use_container_width=True, hide_index=True)

with tab_transactions:
    st.subheader("Record a transaction")
    if accounts.empty:
        st.info("Create an account first.")
    else:
        account_options = {f"Account {int(row['account_id'])} — {row['account_type']} — {row['display_name']}":
                          int(row["account_id"]) for _, row in accounts.iterrows()}
        with st.form("transaction_form"):
            selected_account = st.selectbox("Account", list(account_options.keys()))
            transaction_type = st.selectbox("Type", ["Deposit", "Withdrawal"])
            amount = st.number_input("Amount (₹)", min_value=0.01, value=100.0, step=50.0)
            transaction_date = st.date_input("Transaction date")
            description = st.text_input("Description (optional)", max_chars=200)
            transaction_submit = st.form_submit_button("Record transaction")
        if transaction_submit:
            try:
                tid = record_transaction(account_options[selected_account], transaction_type, amount, transaction_date, description)
                st.success(f"Transaction recorded. ID: {tid}")
                st.rerun()
            except (ValueError, RuntimeError) as exc:
                st.error(str(exc))
    tx = list_transactions()
    st.dataframe(tx, use_container_width=True, hide_index=True)
    if not tx.empty:
        st.download_button("Download transactions CSV", tx.to_csv(index=False).encode("utf-8"),
                           file_name="synthetic_transactions.csv", mime="text/csv")

with tab_reports:
    tx = list_transactions()
    if tx.empty:
        st.info("Record transactions to generate reports.")
    else:
        st.subheader("Monthly summary")
        month_df = monthly_summary(tx)
        st.dataframe(month_df, use_container_width=True, hide_index=True)
        st.subheader("Transaction type summary")
        st.dataframe(transaction_type_summary(tx), use_container_width=True, hide_index=True)
        st.subheader("Rule-based review list")
        flags = review_flags()
        if flags.empty:
            st.success("No transactions met the configured review rule.")
        else:
            st.warning("These records meet a simple review rule; this is not a fraud finding.")
            st.dataframe(flags, use_container_width=True, hide_index=True)
        st.download_button("Download monthly report CSV", month_df.to_csv(index=False).encode("utf-8"),
                           file_name="monthly_summary.csv", mime="text/csv")
