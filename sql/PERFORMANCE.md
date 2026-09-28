# Database Performance Optimization Report

## Problem Statement
Searching transactions by `created_at` timestamp ranges or filtering stuck `PROCESSING` state caused a Full Table Scan on `transactions` table (~50,000+ rows).

## Optimization Strategy
Added compound index targeting filter predicates:
```sql
CREATE INDEX idx_transactions_status_created_at ON transactions (status, created_at);
CREATE INDEX idx_transactions_ref ON transactions (transaction_ref);
