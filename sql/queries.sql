-- 1. Daily Aggregated Volume and Counts
SELECT 
    DATE(created_at) AS tx_date,
    status,
    COUNT(*) AS total_count,
    SUM(amount) AS total_value
FROM transactions
GROUP BY DATE(created_at), status
ORDER BY tx_date DESC, status;

-- 2. Top 10 Customers by Successful Transaction Volume
SELECT 
    c.id AS customer_id,
    c.customer_ref,
    c.name,
    SUM(t.amount) AS total_successful_value
FROM customers c
JOIN transactions t ON c.id = t.customer_id
WHERE t.status = 'SUCCESS'
GROUP BY c.id, c.customer_ref, c.name
ORDER BY total_successful_value DESC
LIMIT 10;

-- 3. Stalled Transactions in PROCESSING > 15 Minutes
SELECT 
    id,
    transaction_ref,
    customer_id,
    amount,
    created_at
FROM transactions
WHERE status = 'PROCESSING'
  AND created_at < NOW() - INTERVAL '15 minutes';

-- 4. Identify Duplicate Transaction References
SELECT 
    transaction_ref,
    COUNT(*) AS occurrence_count
FROM transactions
GROUP BY transaction_ref
HAVING COUNT(*) > 1;

-- 5. Daily Transaction Success Rate (%)
SELECT 
    DATE(created_at) AS tx_date,
    COUNT(*) AS total_tx,
    COUNT(*) FILTER (WHERE status = 'SUCCESS') AS success_tx,
    ROUND((COUNT(*) FILTER (WHERE status = 'SUCCESS')::NUMERIC / COUNT(*)) * 100, 2) AS success_rate_percentage
FROM transactions
GROUP BY DATE(created_at)
ORDER BY tx_date DESC;

-- 6. Transaction & Callback Settlement Reconciliation
SELECT 
    t.status AS tx_status,
    COUNT(DISTINCT t.id) AS tx_count,
    SUM(t.amount) AS tx_total_amount,
    COUNT(DISTINCT cb.id) AS successful_callback_count,
    COALESCE(SUM(cb_tx.amount), 0) AS callback_reconciled_amount
FROM transactions t
LEFT JOIN callbacks cb 
    ON t.id = cb.transaction_id AND cb.callback_status = 'SUCCESS'
LEFT JOIN transactions cb_tx ON cb.transaction_id = cb_tx.id
WHERE t.status = 'SUCCESS'
GROUP BY t.status;

-- 7. Average and p95 Transaction Processing Latency
SELECT 
    AVG(EXTRACT(EPOCH FROM (completed_at - created_at))) AS avg_processing_seconds,
    PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY EXTRACT(EPOCH FROM (completed_at - created_at))) AS p95_processing_seconds
FROM transactions
WHERE completed_at IS NOT NULL;
