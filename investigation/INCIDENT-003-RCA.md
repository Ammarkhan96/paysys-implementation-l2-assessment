# Incident RCA - INCIDENT-003 (Transaction Search Performance Deterioration)

## Root Cause
Missing index on `transaction_ref` forced full database table scans during searches.

## Remediation
Created database index `idx_transactions_ref` and `idx_transactions_status_created_at`.
