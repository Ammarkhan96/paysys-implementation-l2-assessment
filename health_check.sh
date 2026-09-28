#!/usr/bin/env bash
set -euo pipefail

STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/health || echo "000")
if [ "$STATUS" -eq 200 ]; then
    echo "Service Healthy"
    exit 0
else
    echo "Service Unhealthy: $STATUS"
    exit 1
fi
