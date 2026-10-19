---
name: start-local-proxy
description: Use this skill when the user asks to start, restart, or test the local AI proxy environment, router, or dashboard.
---

# Start Local AI Proxy Stack

This skill provides the exact commands needed to restart the various components of the `basisconf` local proxy stack. The TUI interfaces require these to be started in the background on specific ports.

## Components and Ports
- **Grok Proxy**: Port 8000
- **Claude Proxy**: Port 8001
- **Router**: Port 8005
- **Dashboard**: Port 8080

## Steps to Restart

If you need to restart any of these services, first kill the existing process on that port, then start the new one in the background.

### 1. Restart Grok Proxy
```powershell
$pids = (Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue).OwningProcess
if ($pids) { Stop-Process -Id $pids -Force -ErrorAction SilentlyContinue }
python cli_proxy_server.py --provider grok --protocol ollama --port 8000
```

### 2. Restart Claude Proxy
```powershell
$pids = (Get-NetTCPConnection -LocalPort 8001 -ErrorAction SilentlyContinue).OwningProcess
if ($pids) { Stop-Process -Id $pids -Force -ErrorAction SilentlyContinue }
python cli_proxy_server.py --provider claude --protocol ollama --port 8001
```

### 3. Restart Router
```powershell
$pids = (Get-NetTCPConnection -LocalPort 8005 -ErrorAction SilentlyContinue).OwningProcess
if ($pids) { Stop-Process -Id $pids -Force -ErrorAction SilentlyContinue }
python local_router.py --port 8005
```

### 4. Restart Dashboard
```powershell
$pids = (Get-NetTCPConnection -LocalPort 8080 -ErrorAction SilentlyContinue).OwningProcess
if ($pids) { Stop-Process -Id $pids -Force -ErrorAction SilentlyContinue }
python -m tokenbuffet.dashboard
```
