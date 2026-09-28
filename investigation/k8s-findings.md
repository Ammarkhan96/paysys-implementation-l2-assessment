# Kubernetes Starter Manifest Defect Analysis (`broken-api.yaml`)

## Identified Defect Findings:
1. **Port Mismatch in Readiness Probe:** Readiness check was configured on port `8081` while container exposes port `8080`.
   - *Fix:* Aligned probe port to `8080`.
2. **Service Label Selector Mismatch:** Service selector had `app: minipay-backend` while deployment labels used `app: minipay-api`.
   - *Fix:* Corrected selector key to `app: minipay-api`.
3. **Placeholder Image Reference:** Image reference was specified as `YOUR_IMAGE_HERE`.
   - *Fix:* Replaced with tag `minipay-api:v1.0.0`.
