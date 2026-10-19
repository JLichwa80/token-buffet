"""Local status and configuration UI for the CLI bridge."""

import http.server
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import time
import urllib.parse
import webbrowser
from pathlib import Path

from tokenbuffet import loopback

PORT = int(os.environ.get("TOKENBUFFET_DASHBOARD_PORT", "8080"))
ROOT = Path.cwd()  # launched with cwd=workspace by cli.py
LOG_DIR = ROOT / "logs"
STATUS_DIR = ROOT / "data" / "providers_status"
REGISTRY = ROOT / "registered_providers"
APP_DIR = ROOT / "registered_apps"
INTEGRATIONS = ROOT / "integrations"
ROUTER_CONFIG = ROOT / "config" / "router_config.json"
STATIC_DIR = Path(__file__).parent / "static"
INDEX_FILE = STATIC_DIR / "index.html"
CSS_FILE = STATIC_DIR / "app.css"
JS_FILE = STATIC_DIR / "app.js"

STATIC_FILES = {
    "/": (INDEX_FILE, "text/html; charset=utf-8"),
    "/index.html": (INDEX_FILE, "text/html; charset=utf-8"),
    "/app.css": (CSS_FILE, "text/css; charset=utf-8"),
    "/dashboard.css": (CSS_FILE, "text/css; charset=utf-8"),
    "/app.js": (JS_FILE, "application/javascript; charset=utf-8"),
    "/dashboard.js": (JS_FILE, "application/javascript; charset=utf-8"),
    "/logo_light.png": (STATIC_DIR / "logo_light.png", "image/png"),
    "/logo_dark.png": (STATIC_DIR / "logo_dark.png", "image/png"),
}


def read_json(path, default=None):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def listening(port):
    try:
        return loopback.listening(port, timeout=0.15)
    except (ValueError, TypeError):
        return False


def provider_config(name):
    if not isinstance(name, str) or name not in provider_names():
        raise ValueError("Unknown provider")
    return REGISTRY / name / "config.json"


def provider_names():
    return {p.parent.name for p in REGISTRY.glob("*/config.json")}


def provider_rows():
    rows = []
    for name in sorted(provider_names()):
        config = read_json(provider_config(name), {})
        status = read_json(STATUS_DIR / f"{name}_run_status.json", {})
        usage = read_json(STATUS_DIR / f"{name}_usage.json", {}).get("usage", {})
        models = read_json(STATUS_DIR / f"{name}_models.json", {}).get("models", {})
        port = status.get("port") or config.get("server", {}).get("port")
        reachable = listening(port) if status.get("status") == "running" else False
        current_status = status.get("status", "unknown")
        if current_status == "running" and not reachable:
            current_status = "unreachable"
        rows.append({
            "name": name, "port": port, "pid": status.get("pid"),
            "status": current_status, "running": reachable,
            "reason": status.get("reason"), "limits": usage.get("limits", {}),
            "usage_state": (status.get("usage") or {}).get("state"),
            "usage_reason": (status.get("usage") or {}).get("reason"),
            "plan": usage.get("plan"), "gathered_at": usage.get("gathered_at"),
            "models": models.get("available", []), "tools": config.get("tools", {}),
            "tiers": config.get("tiers", {}),
        })
    return rows


def installed_app_types():
    from tokenbuffet.onboarding import check_app_type
    return {p.parent.name for p in INTEGRATIONS.glob("*/app_config.json") if not check_app_type(p.parent.name)}


def app_rows():
    from tokenbuffet.onboarding import can_open
    rows = []
    installed = installed_app_types()
    openable = {t: can_open(t) for t in installed}
    for config_path in sorted(APP_DIR.glob("*/*/app_config.json")):
        config = read_json(config_path)
        if not isinstance(config, dict) or config_path.parent.parent.name not in installed:
            continue
        app_path = Path(config.get("path") or config_path.parent)
        if not app_path.is_absolute():
            app_path = (config_path.parent / app_path).resolve()
        target = app_path / (config.get("bridge_configuration") or "app_settings.json")
        category = config_path.parent.parent.name
        declared_type = config.get("type") or category
        name = config.get("name") or config_path.parent.name
        label = config.get("label") or name
        rows.append({
            "name": name,
            "label": label,
            "type": declared_type,
            "category": category,
            "dir": config_path.parent.name,
            "can_open": openable[category],
            "instance": str(config_path.parent),
            "path": str(app_path),
            "bridge_configuration": config.get("bridge_configuration"),
            "target": str(target),
            "target_exists": target.exists(),
            "vault_type": config.get("vault_type"),
        })
    return rows


def app_types():
    result = []
    installed = installed_app_types()
    for path in sorted(INTEGRATIONS.glob("*/app_config.json")):
        if path.parent.name.startswith("_") or path.parent.name not in installed:
            continue
        config = read_json(path, {})
        presets = read_json(path.parent / "vault_types.json", {})
        directory = config.get("presets_directory")
        choices = (sorted(p.parent.name for p in (path.parent / directory).glob("*/app_config.json"))
                   if directory else sorted(presets) if isinstance(presets, dict) else [])
        result.append({"name": path.parent.name,
                       "title": config.get("title") or path.parent.name,
                       "description": config.get("description", ""),
                       "bridge_configuration": config.get("bridge_configuration", "app_settings.json"),
                       "presets": choices,
                       "preset_field": "preset" if directory else "vault_type",
                       "preset_label": config.get("preset_label", "Vault Preset"),
                       "path_required": config.get("path") == "[app_path]"})
    return result


def router_events(request_ids):
    events = {}
    path = LOG_DIR / "router" / "router.log"
    try:
        with path.open(encoding="utf-8", errors="replace") as stream:
            for line in stream:
                match = re.search(r"\b(ROUTE|FAIL|DONE|REQUEST) id=([\w-]+)", line)
                if match and match.group(2) in request_ids:
                    events[match.group(2)] = {"event": match.group(1), "detail": line.strip()[:300]}
    except OSError:
        pass
    return events


def activity_rows(limit=30):
    paths = []
    for path in LOG_DIR.glob("*/proxy/sessions/req_*.log"):
        try:
            paths.append((path.stat().st_mtime, path))
        except OSError:
            continue
    paths.sort(key=lambda item: item[0], reverse=True)
    paths = paths[:limit]
    events = router_events({path.stem.rsplit("_", 1)[-1] for _, path in paths})
    rows = []
    for modified, path in paths:
        request_id = path.stem.rsplit("_", 1)[-1]
        row = {"id": request_id, "provider": path.parents[2].name,
               "when": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(modified)),
               "status": "In progress", "model": "Unknown", "path": "Unknown",
               "app": "Unknown", "router": events.get(request_id)}
        try:
            with path.open(encoding="utf-8", errors="replace") as stream:
                for line in stream:
                    summary = line.split("] ", 1)[-1].strip()
                    if summary.startswith(">>> POST "):
                        row["path"] = summary[9:]
                    elif summary.startswith("Request parsed:"):
                        match = re.search(r"model=([^,]+)", summary)
                        if match:
                            row["model"] = match.group(1)
                    elif summary.startswith("Proxy Error:"):
                        row["status"] = "Failed"
                        row["reason"] = summary[13:][:240]
                    elif summary.startswith("Output received:") and row["status"] != "Failed":
                        row["status"] = "Completed"
        except OSError:
            row["status"] = "Unavailable"
        rows.append(row)
    return rows


def addable_providers():
    from tokenbuffet.onboarding import known_providers
    return [n for n in known_providers() if n not in provider_names()]


def add_provider(data):
    from tokenbuffet.onboarding import add_known_provider
    name = data.get("provider")
    try:
        result = add_known_provider(name)
    except (FileNotFoundError, FileExistsError) as exc:
        raise ValueError(str(exc))
    return {"added": name, "path": result["path"]}


def validate_provider_action(data):
    from tokenbuffet.onboarding import validate_provider
    name = data.get("provider")
    provider_config(name)  # rejects unknown names
    result = validate_provider(name)
    if not result["success"]:
        raise ValueError(f"{result['error']} {result['hint']}".strip())
    return result


HISTORY_FILE = ROOT / "data" / "quota_history.jsonl"
HISTORY_MIN_INTERVAL = 300
HISTORY_MAX_BYTES = 2 * 1024 * 1024
_history_last = {}


def record_quota_history(providers):
    """Append a remaining-quota snapshot per provider when it changed or 5 minutes passed."""
    now = time.time()
    lines = []
    for row in providers:
        remaining = {period: v["remaining_pct"] for period, v in (row.get("limits") or {}).items()
                     if isinstance(v, dict) and isinstance(v.get("remaining_pct"), (int, float))}
        if not remaining:
            continue
        last = _history_last.get(row["name"])
        if last and last[1] == remaining and now - last[0] < HISTORY_MIN_INTERVAL * 6:
            continue
        if last and now - last[0] < HISTORY_MIN_INTERVAL:
            continue
        _history_last[row["name"]] = (now, remaining)
        lines.append(json.dumps({"t": int(now), "provider": row["name"], "remaining": remaining}))
    if not lines:
        return
    try:
        HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        if HISTORY_FILE.exists() and HISTORY_FILE.stat().st_size > HISTORY_MAX_BYTES:
            kept = HISTORY_FILE.read_text(encoding="utf-8").splitlines()[-5000:]
            HISTORY_FILE.write_text("\n".join(kept) + "\n", encoding="utf-8")
        with open(HISTORY_FILE, "a", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
    except OSError:
        pass


def quota_history(name, days=7):
    if name not in provider_names():
        raise ValueError("Unknown provider")
    cutoff = time.time() - max(1, min(int(days), 90)) * 86400
    points = []
    try:
        for line in HISTORY_FILE.read_text(encoding="utf-8").splitlines():
            try:
                row = json.loads(line)
            except ValueError:
                continue
            if row.get("provider") == name and row.get("t", 0) >= cutoff:
                points.append({"t": row["t"], "remaining": row.get("remaining", {})})
    except OSError:
        pass
    return {"name": name, "points": points}


def dashboard_state():
    providers = provider_rows()
    record_quota_history(providers)
    return {"providers": providers, "apps": app_rows(), "app_types": app_types(),
            "router": read_json(ROUTER_CONFIG, {}), "router_running": listening(8090),
            "dashboard_running": True, "activity": activity_rows(), "root": str(ROOT),
            "addable_providers": addable_providers(), "time": time.time()}


def save_router(data):
    if not isinstance(data, dict) or data.get("mode") not in ("usage", "custom"):
        raise ValueError("Mode must be usage or custom")
    names = provider_names()
    order = data.get("custom_order")
    providers = data.get("providers")
    if (not isinstance(order, list) or any(not isinstance(name, str) for name in order)
            or len(order) != len(set(order)) or any(name not in names for name in order)):
        raise ValueError("Custom order must contain unique registered providers")
    if not isinstance(providers, dict) or any(name not in names for name in providers):
        raise ValueError("Router mappings contain an unknown provider")
    for name, mapping in providers.items():
        tiers = mapping.get("tiers") if isinstance(mapping, dict) else None
        if not isinstance(tiers, dict):
            raise ValueError(f"Invalid tiers for {name}")
        available = read_json(STATUS_DIR / f"{name}_models.json", {}).get("models", {}).get("available", [])
        ids = {item.get("id") if isinstance(item, dict) else item for item in available}
        for tier, model in tiers.items():
            if not isinstance(tier, str) or not tier or not isinstance(model, str) or model not in ids:
                raise ValueError(f"{name}/{tier}: model must be an available CLI model ID")
    current = read_json(ROUTER_CONFIG, {})
    current.update(mode=data["mode"], custom_order=order, providers=providers)
    if "effort" in data and isinstance(data["effort"], dict):
        current["effort"] = data["effort"]
    current.pop("tiers", None)
    write_json(ROUTER_CONFIG, current)
    return {"saved": True, "restart_required": listening(8090)}


def set_tool(data):
    path = provider_config(data.get("provider"))
    config = read_json(path)
    tools = config.get("tools", {})
    tool = data.get("tool")
    if tool not in tools.get("available", []) or not isinstance(data.get("enabled"), bool):
        raise ValueError("Choose an available tool and enabled=true or false")
    enabled = set(tools.get("enabled", []))
    if data["enabled"]:
        enabled.add(tool)
    else:
        enabled.discard(tool)
    tools["enabled"] = [item for item in tools["available"] if item in enabled]
    config["tools"] = tools
    write_json(path, config)
    return {"saved": True, "restart_required": True}


def register_app(data):
    app = data.get("type")
    name = data.get("name")
    app_path = data.get("path") or ""
    extras = {}
    for key in ("vault_type", "bridge_configuration", "label", "preset"):
        if data.get(key):
            extras[key] = data[key]
    if not all(isinstance(value, str) for value in (app, name, app_path, *extras.values())):
        raise ValueError("Registration fields must be text")
    command = [sys.executable, str(INTEGRATIONS / "register.py"), app, name, app_path]
    command += [f"{key}={value}" for key, value in extras.items()]
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=120)
    if result.returncode:
        raise RuntimeError((result.stderr or result.stdout).strip()[-600:])
    return json.loads(result.stdout)


def apply_app(data):
    app, name = data.get("type"), data.get("name")
    if not all(isinstance(x, str) and x and Path(x).name == x and x not in (".", "..") for x in (app, name)):
        raise ValueError("Invalid app instance")
    command = [sys.executable, str(INTEGRATIONS / "register.py"), app, name, "--reapply"]
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=120)
    if result.returncode:
        raise RuntimeError((result.stderr or result.stdout).strip()[-600:])
    return json.loads(result.stdout)


def pick_folder(data):
    result = subprocess.run([sys.executable, "-m", "tokenbuffet.folder_picker"], capture_output=True, text=True, timeout=300)
    if result.returncode:
        raise RuntimeError((result.stderr or result.stdout).strip()[-600:])
    return {"path": result.stdout.strip()}


def open_app_instance(data):
    from tokenbuffet.onboarding import open_app
    app, name = data.get("type"), data.get("name")
    if not all(isinstance(x, str) and x and Path(x).name == x and x not in (".", "..") for x in (app, name)):
        raise ValueError("Invalid app instance")
    return {"opened": open_app(app, name)}


def launch_provider(data):
    name = data.get("provider")
    config = read_json(provider_config(name), {})
    status = read_json(STATUS_DIR / f"{name}_run_status.json", {})
    if status.get("status") == "running" and listening(status.get("port")):
        raise ValueError(f"{name} is already running on port {status['port']}")
    req_port = data.get("port")
    if isinstance(req_port, int) and 1024 <= req_port <= 65535:
        if req_port != config.get("server", {}).get("port"):
            config.setdefault("server", {})["port"] = req_port
            write_json(provider_config(name), config)
    port = config.get("server", {}).get("port")
    if not isinstance(port, int) or not 1 <= port <= 65535:
        raise ValueError("Provider has no valid configured port")
    if listening(port):
        raise ValueError(f"Port {port} is already in use")
    flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
    output = (LOG_DIR / name / "proxy" / "console.log")
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("a", encoding="utf-8") as stream:
        process = subprocess.Popen([sys.executable, "-m", "tokenbuffet.cli_proxy_server",
                                    "--provider", name, "--port", str(port)], cwd=ROOT,
                                    stdout=stream, stderr=subprocess.STDOUT, creationflags=flags)
    return {"started": True, "pid": process.pid, "port": port, "state": "starting"}


def restart_provider(data):
    name = data.get("provider")
    status = read_json(STATUS_DIR / f"{name}_run_status.json", {})
    if status.get("status") == "running" and listening(status.get("port")):
        try:
            stop_provider(data)
            time.sleep(0.8)
        except Exception:
            pass
    return launch_provider(data)


def stop_provider(data):
    name = data.get("provider")
    provider_config(name)
    status = read_json(STATUS_DIR / f"{name}_run_status.json", {})
    pid = status.get("pid")
    if status.get("status") != "running" or not isinstance(pid, int) or not listening(status.get("port")):
        raise ValueError("No confirmed running provider process")
    if os.name == "nt":
        result = subprocess.run(["powershell", "-NoProfile", "-Command",
                                 "(Get-CimInstance Win32_Process -Filter 'ProcessId=" + str(pid) + "').CommandLine"],
                                 capture_output=True, text=True, timeout=10)
        command = result.stdout
    else:
        command = Path(f"/proc/{pid}/cmdline").read_bytes().replace(b"\0", b" ").decode(errors="replace")
    if "tokenbuffet.cli_proxy_server" not in command or not re.search(r"--provider\s+" + re.escape(name) + r"(?:\s|$)", command):
        raise ValueError("Process identity does not match the provider")
    if os.name == "nt":
        result = subprocess.run(["taskkill", "/PID", str(pid), "/T"], capture_output=True, text=True, timeout=10)
        if result.returncode:
            raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    else:
        os.kill(pid, signal.SIGTERM)
    return {"stopping": True, "pid": pid}


def login_provider(data):
    name = data.get("provider")
    config = read_json(provider_config(name), {})
    command = config.get("usage", {}).get("cli_cmd", [])
    if not isinstance(command, list) or not command or not isinstance(command[0], str) or not shutil.which(command[0]):
        raise ValueError("Provider CLI is unavailable")
    # Login uses only the executable, never the capture flags.
    if os.name == "nt":
        process = subprocess.Popen(["cmd.exe", "/k", shutil.which(command[0])], cwd=ROOT,
                                   creationflags=subprocess.CREATE_NEW_CONSOLE)
    elif sys.platform == "darwin":
        process = subprocess.Popen(["open", "-a", "Terminal", command[0]], cwd=ROOT)
    else:
        raise ValueError("Open the provider CLI in a terminal on this system")
    return {"opened": True, "pid": process.pid}


def _running(name):
    status = read_json(STATUS_DIR / f"{name}_run_status.json", {})
    return status.get("status") == "running" and listening(status.get("port"))


def start_providers(data):
    started, skipped = [], []
    for name in sorted(provider_names()):
        if _running(name):
            skipped.append(name)
            continue
        try:
            launch_provider({"provider": name})
            started.append(name)
        except ValueError as exc:
            skipped.append(f"{name} ({exc})")
    return {"launched": True, "output": f"Started: {', '.join(started) or 'none'}. Skipped: {', '.join(skipped) or 'none'}"}


def stop_providers(data):
    stopped = []
    for name in sorted(provider_names()):
        if _running(name):
            try:
                stop_provider({"provider": name})
                stopped.append(name)
            except (ValueError, RuntimeError, OSError):
                pass
    return {"done": True, "output": f"Stopping: {', '.join(stopped) or 'none running'}"}


def start_router(data):
    status = read_json(STATUS_DIR / "router_run_status.json", {})
    if status.get("status") == "running" and listening(status.get("port")):
        raise ValueError(f"Router is already running on port {status['port']}")
    if listening(8090):
        raise ValueError("Port 8090 is already in use")
    flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
    output = LOG_DIR / "router" / "console.log"
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("a", encoding="utf-8") as stream:
        process = subprocess.Popen([sys.executable, "-m", "tokenbuffet.local_router", "--port", "8090"],
                                   cwd=ROOT, stdout=stream, stderr=subprocess.STDOUT, creationflags=flags)
    return {"launched": True, "output": f"Router starting on port 8090 (pid {process.pid})"}


def stop_router(data):
    status = read_json(STATUS_DIR / "router_run_status.json", {})
    pid = status.get("pid")
    if not isinstance(pid, int) or not listening(status.get("port")):
        raise ValueError("No confirmed running router process")
    if os.name == "nt":
        result = subprocess.run(["taskkill", "/PID", str(pid), "/T"], capture_output=True, text=True, timeout=10)
        if result.returncode:
            raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    else:
        os.kill(pid, signal.SIGTERM)
    return {"done": True, "output": f"Router stopping (pid {pid})"}


def refresh_providers(data):
    import urllib.request
    refreshed = []
    for name in sorted(provider_names()):
        status = read_json(STATUS_DIR / f"{name}_run_status.json", {})
        if not _running(name):
            continue
        for op in ("usage", "models"):
            try:
                urllib.request.urlopen(loopback.url(status['port'], f"/{op}"), timeout=190).read()
            except OSError:
                break
        else:
            refreshed.append(name)
    return {"launched": True, "output": f"Refreshed: {', '.join(refreshed) or 'none'}"}


def start_all(data):
    p = start_providers(data)
    time.sleep(1.0)
    try:
        r = start_router(data)
    except ValueError as exc:
        r = {"output": str(exc)}
    return {"launched": True, "output": f"{p['output']} | Router: {r['output']}"}


def stop_all(data):
    out = []
    for fn in (stop_router, stop_providers):
        try:
            out.append(fn(data)["output"])
        except (ValueError, RuntimeError, OSError) as exc:
            out.append(str(exc))
    return {"done": True, "output": " | ".join(out)}


def log_tail(name, lines=200):
    """Last `lines` lines of a provider's proxy console log, or the router log."""
    if name == "router":
        path = LOG_DIR / "router" / "router.log"
        if not path.is_file():
            path = LOG_DIR / "router" / "console.log"
    elif name in provider_names():
        path = LOG_DIR / name / "proxy" / "console.log"
    else:
        raise ValueError("Unknown log source")
    lines = max(1, min(int(lines), 1000))
    try:
        with open(path, "rb") as f:
            f.seek(0, os.SEEK_END)
            size = f.tell()
            f.seek(max(0, size - 256 * 1024))
            text = f.read().decode("utf-8", errors="replace")
    except OSError:
        return {"name": name, "lines": []}
    return {"name": name, "lines": text.splitlines()[-lines:]}


class DashboardHandler(http.server.BaseHTTPRequestHandler):
    def json_response(self, status, body):
        payload = json.dumps(body, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):
        if self.path == "/api/state":
            self.json_response(200, dashboard_state())
        elif self.path.startswith("/api/history"):
            query = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            try:
                self.json_response(200, quota_history(query.get("name", [""])[0],
                                                      query.get("days", ["7"])[0]))
            except ValueError as exc:
                self.json_response(400, {"error": str(exc)})
        elif self.path.startswith("/api/logs"):
            query = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            try:
                self.json_response(200, log_tail(query.get("name", [""])[0],
                                                 query.get("lines", ["200"])[0]))
            except ValueError as exc:
                self.json_response(400, {"error": str(exc)})
        elif self.path in STATIC_FILES:
            target_path, content_type = STATIC_FILES[self.path]
            try:
                payload = target_path.read_bytes()
            except OSError:
                self.json_response(500, {"error": f"{target_path.name} is missing"})
                return
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(payload)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(payload)
        else:
            self.json_response(404, {"error": "Unknown endpoint"})

    def do_POST(self):
        origin = self.headers.get("Origin")
        if origin and origin != loopback.url(PORT):
            self.json_response(403, {"error": "Origin is not local dashboard"})
            return
        actions = {"/api/router": save_router, "/api/providers/tools": set_tool,
                   "/api/apps/register": register_app, "/api/apps/apply": apply_app,
                   "/api/apps/open": open_app_instance, "/api/apps/pick-folder": pick_folder,
                   "/api/providers/add": add_provider, "/api/providers/validate": validate_provider_action,
                   "/api/providers/launch": launch_provider, "/api/providers/stop": stop_provider,
                   "/api/providers/restart": restart_provider,
                   "/api/providers/login": login_provider,
                   "/api/control/providers": start_providers, "/api/control/providers-stop": stop_providers,
                   "/api/control/router": start_router, "/api/control/router-stop": stop_router,
                   "/api/control/refresh": refresh_providers,
                   "/api/control/all-start": start_all, "/api/control/all-stop": stop_all}
        action = actions.get(self.path)
        if action is None:
            self.json_response(404, {"error": "Unknown endpoint"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= 65536:
                raise ValueError("Invalid request size")
            data = json.loads(self.rfile.read(length))
            if not isinstance(data, dict):
                raise ValueError("Expected a JSON object")
            self.json_response(200, action(data))
        except (ValueError, FileNotFoundError, TimeoutError) as exc:
            self.json_response(400, {"error": str(exc)})
        except (OSError, RuntimeError, subprocess.TimeoutExpired) as exc:
            self.json_response(500, {"error": str(exc)})

    def log_message(self, format, *args):
        pass


def _publish_dashboard_status(state, port):
    STATUS_DIR.mkdir(parents=True, exist_ok=True)
    status_path = STATUS_DIR / "dashboard_run_status.json"
    value = {"status": state, "port": port, "pid": os.getpid()}
    tmp = status_path.with_suffix(".tmp")
    tmp.write_text(json.dumps(value), encoding="utf-8")
    os.replace(tmp, status_path)


def main():
    global PORT
    running_port = loopback.already_running(STATUS_DIR / "dashboard_run_status.json")
    if running_port:
        print(f"Dashboard is already running: {loopback.url(running_port)}", file=sys.stderr)
        sys.exit(1)
    try:
        server = loopback.serve_next(PORT, DashboardHandler)
    except OSError as exc:
        print(f"Cannot start dashboard: {exc}", file=sys.stderr)
        sys.exit(1)
    if server.server_address[1] != PORT:
        print(f"Port {PORT} is taken by another process; dashboard is using {server.server_address[1]}.")
        PORT = server.server_address[1]
    url = loopback.url(PORT)
    print(f"Dashboard: {url}")
    _publish_dashboard_status("running", PORT)
    if not os.environ.get("TOKENBUFFET_NO_BROWSER"):
        webbrowser.open(url)
    server.serve_forever()


if __name__ == "__main__":
    main()
