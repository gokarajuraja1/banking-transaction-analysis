# Project notes

## Design
- MySQL stores synthetic customers, accounts, and transaction rows.
- Account balance is calculated from opening balance plus deposits minus withdrawals.
- Withdrawal validation prevents the simulated balance from becoming negative.
- The review rule flags transactions at or above a configurable amount threshold. It is a manual-review aid, not a fraud classifier.
- SQL statements use parameters for user-supplied values.
- `.env` holds local configuration and must not be committed.

## Known limitations
- The shared-password gate is only a basic classroom demo, not production authentication.
- No real payment rails, external bank APIs, or real credentials are used.
- For a deployed system, use individual authenticated users, role-based permissions, secure secret management, auditing, and stronger operational controls.
