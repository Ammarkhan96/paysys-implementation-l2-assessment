# Incident RCA - INCIDENT-002 (Application Unavailable Post-Deployment)

## Root Cause
Kubernetes Service selector mismatched Deployment pod labels (`app: minipay-backend` vs `app: minipay-api`).

## Remediation
Updated service selector to target correct pod labels `app: minipay-api`.
