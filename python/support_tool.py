#!/usr/bin/env python3
import sys
import os
import argparse
import json
import psycopg2
from psycopg2.extras import RealDictCursor

def run_diagnostic(tx_ref):
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", 5432)),
            dbname=os.getenv("DB_NAME", "minipay"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "postgres"),
            connect_timeout=3
        )
    except Exception as err:
        return {"error": f"Database connection failed: {str(err)}"}

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT t.id, t.transaction_ref, t.amount, t.status, t.created_at, t.completed_at,
                       c.customer_ref, c.name as customer_name
                FROM transactions t
                JOIN customers c ON t.customer_id = c.id
                WHERE t.transaction_ref = %s;
            """, (tx_ref,))
            tx = cur.fetchone()

            if not tx:
                return {"error": f"Transaction '{tx_ref}' not found."}

            cur.execute("""
                SELECT attempt_no, http_status, callback_status 
                FROM callbacks 
                WHERE transaction_id = %s 
                ORDER BY attempt_no DESC;
            """, (tx["id"],))
            callbacks = cur.fetchall()

            issues = []
            action = "No intervention required."

            if tx["status"] == "PROCESSING":
                issues.append("Transaction stalled in PROCESSING state.")
                action = "Re-queue payment status webhook or issue gateway query."
            elif tx["status"] == "FAILED":
                issues.append("Transaction marked as FAILED.")
                action = "Review gateway response payload for root error code."

            return {
                "transaction_ref": tx["transaction_ref"],
                "customer": tx["customer_name"],
                "amount": float(tx["amount"]),
                "status": tx["status"],
                "callbacks": [dict(c) for c in callbacks],
                "issues_found": issues,
                "recommended_action": action
            }
    finally:
        conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="L2 Transaction Diagnostic CLI")
    parser.add_argument("--transaction", required=True, help="Transaction Reference ID")
    parser.add_argument("--json", action="store_true", help="Format output as JSON")
    args = parser.parse_args()

    result = run_diagnostic(args.transaction)
    
    if args.json:
        print(json.dumps(result, indent=2, default=str))
    else:
        print(f"\n--- Diagnostic Result for {args.transaction} ---")
        print(f"Status: {result.get('status')}")
        print(f"Issues: {result.get('issues_found')}")
        print(f"Action: {result.get('recommended_action')}\n")
