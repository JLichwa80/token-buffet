#!/usr/bin/env python3
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


def check():
    if not shutil.which("claude"):
        raise FileNotFoundError("Claude Code must be installed and available on PATH to open Claudia")


def launch(app_path):
    check()
    target = Path(app_path).resolve()
    if not target.is_dir() or not (target / "CLAUDE.md").is_file():
        raise FileNotFoundError(f"Claudia workspace not found: {target}")
    if sys.platform == "darwin":
        from tokenbuffet.platforms.macos.terminal import launch as launch_terminal
        launch_terminal(["claude"], target)
        return
    if os.name != "nt":
        raise ValueError(f"Open a terminal in {target} and run claude on this system")
    subprocess.Popen(["powershell.exe", "-NoLogo", "-NoExit", "-Command", "claude"],
                     cwd=target, creationflags=subprocess.CREATE_NEW_CONSOLE)


def prepare_demo(app_path):
    """Install Claudia's memory system and host integration with its own installer, then re-apply the router endpoint."""
    npx = shutil.which("npx")
    if not npx:
        raise FileNotFoundError("Node.js (npx) must be installed and available on PATH to install Claudia")
    target = Path(app_path).resolve()
    install = [npx, "get-claudia", "claude", ".", "--yes"]
    result = subprocess.run(install, cwd=target)
    if result.returncode:
        raise RuntimeError(f"npx get-claudia failed with exit code {result.returncode}")
    # The installer looks for venv\Scripts\pip without .exe, so on Windows it skips installing the daemon, writing .mcp.json and the
    # health check. An extension-less copy of pip.exe satisfies it; run the installer again so those steps happen.
    venv_scripts = Path.home() / ".claudia" / "daemon" / "venv" / "Scripts"
    if os.name == "nt" and (venv_scripts / "pip.exe").is_file() and not (venv_scripts / "pip").exists():
        shutil.copyfile(venv_scripts / "pip.exe", venv_scripts / "pip")
        result = subprocess.run(install, cwd=target)
        if result.returncode:
            raise RuntimeError(f"npx get-claudia failed with exit code {result.returncode}")
    mcp_path = target / ".mcp.json"
    if "claudia-memory" not in json.loads(mcp_path.read_text(encoding="utf-8")).get("mcpServers", {}):
        raise RuntimeError(f"Claudia installer did not add claudia-memory to {mcp_path}")
    # The installer also lists gmail, google-calendar and google_workspace; the demo starts with memory only.
    mcp = json.loads(mcp_path.read_text(encoding="utf-8"))
    mcp["mcpServers"] = {"claudia-memory": mcp["mcpServers"]["claudia-memory"]}
    mcp_path.write_text(json.dumps(mcp, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    # Claude Code ignores the workspace's settings.local.json (the MCP approval) until the folder is trusted.
    claude_json = Path.home() / ".claude.json"
    state = json.loads(claude_json.read_text(encoding="utf-8")) if claude_json.exists() else {}
    state.setdefault("projects", {}).setdefault(target.as_posix(), {})["hasTrustDialogAccepted"] = True
    claude_json.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
    init(app_path)


def init(app_path=None):
    folder = Path(__file__).resolve().parent
    config = json.loads((folder / "app_config.json").read_text(encoding="utf-8"))
    target = Path(app_path) if app_path else Path(config.get("path") or ".")
    if not target.is_absolute():
        target = (Path.cwd() if app_path else folder) / target
    target = target / config.get("bridge_configuration", ".claude/settings.local.json")
    settings = json.loads((folder / "app_settings.json").read_text(encoding="utf-8"))
    data = json.loads(target.read_text(encoding="utf-8")) if target.exists() else {}
    env = data.setdefault("env", {})
    env.update(settings.pop("env", {}))
    client = config["client_settings"]
    env["ANTHROPIC_BASE_URL"] = client["active_endpoint"].removesuffix("/").removesuffix("/v1")
    data.update(settings)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
