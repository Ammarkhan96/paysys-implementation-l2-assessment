# Linux System Diagnostics

## Diagnostic Execution Output
```bash
# OS Version & Kernel
uname -a

# CPU & Memory
free -m
top -b -n 1 | head -n 20

# Listening Ports
ss -tulpn
