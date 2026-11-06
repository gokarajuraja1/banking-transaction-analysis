-- Optional starter data. Run once only, to avoid duplicate sample records.
INSERT INTO customers (display_name) VALUES
('Sample Customer A'), ('Sample Customer B');

INSERT INTO accounts (customer_id, account_type, opening_balance) VALUES
(1, 'Savings', 10000.00), (1, 'Student', 2500.00), (2, 'Current', 20000.00);

INSERT INTO transactions (account_id, transaction_date, transaction_type, amount, description) VALUES
(1, '2026-01-05', 'Deposit', 1500.00, 'Synthetic salary deposit'),
(1, '2026-01-08', 'Withdrawal', 400.00, 'Synthetic grocery expense'),
(2, '2026-02-10', 'Deposit', 800.00, 'Synthetic allowance'),
(3, '2026-02-14', 'Withdrawal', 1200.00, 'Synthetic office expense'),
(3, '2026-03-02', 'Deposit', 60000.00, 'Synthetic large deposit for review demo');
