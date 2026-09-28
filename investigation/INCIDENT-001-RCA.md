# Incident RCA - INCIDENT-001 (Intermittent HTTP 500 Search Failure)

## Root Cause
Uncaught `NullPointerException` when processing null timestamps on active `PROCESSING` transactions where `completed_at` is `NULL`.

## Remediation
Added null guard checks in response serialization logic.
