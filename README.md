# Banking Transaction Analysis System

An educational Python + MySQL + Streamlit project using synthetic data. It records sample customers, accounts, deposits and withdrawals, then produces account-wise and monthly summaries, charts, CSV exports, and rule-based review flags.

> **Safety boundary:** This is not a real banking platform. Use synthetic records only. Account balances are simulated. Review flags indicate only that a rule was matched; they do not assert fraud.

## Features
- Customer and account records
- Deposit/withdrawal validation
- Simulated balance calculations
- Account-wise and monthly summaries
- Pandas grouping, NumPy statistics, Matplotlib charts
- CSV export and configurable review threshold
- Parameterized SQL queries and environment-based configuration
- Basic shared-password gate for a classroom demo

## Requirements
- Python 3.10+
- MySQL Server 8.x
- A terminal (PowerShell, Command Prompt, or terminal in VS Code)

## Setup

1. Create a MySQL database and application user. Run the following as a MySQL administrator, changing the password:
   ```sql
   CREATE DATABASE banking_analysis;
   CREATE USER 'banking_app'@'localhost' IDENTIFIED BY 'change_this_password';
   GRANT SELECT, INSERT, UPDATE, DELETE, CREATE ON banking_analysis.* TO 'banking_app'@'localhost';
   FLUSH PRIVILEGES;
   ```
2. In MySQL Workbench, open and execute `database/schema.sql` while connected to `banking_analysis`.
3. Copy `.env.example` to `.env` and edit the values to match your local MySQL setup. Never commit `.env`.
4. Create and activate a virtual environment:
   - Windows PowerShell:
     ```powershell
     py -m venv .venv
     Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
     .\.venv\Scripts\Activate.ps1
     ```
   - Command Prompt:
     ```bat
     py -m venv .venv
     .venv\Scripts\activate.bat
     ```
5. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```
6. Start the app:
   ```bash
   streamlit run app.py
   ```
7. Enter the `APP_PASSWORD` value from `.env` when prompted.

## Tests
Run:
```bash
python -m pytest -q
```

## Git and GitHub
From the project root:
```bash
git init
git add .
git commit -m "Initial banking transaction analysis project"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/banking-transaction-analysis.git
git push -u origin main
```
Create an empty repository on GitHub first and replace `YOUR-USERNAME` with your GitHub username. Do not upload `.env`, database passwords, real financial information, or customer data.

## Review rule
Transactions at or above `REVIEW_AMOUNT_THRESHOLD` are marked for manual review. This simple threshold is illustrative only and is not a fraud detector.
