#!/usr/bin/env python3
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


def check():
    """Raise if Abject is not installed (https://abject.world/install)."""
    if not shutil.which("abject"):
        raise ValueError("Abject is not installed; run: tbuffet install-abject")


def install():
    """Install the headless (command-line) edition of Abject with its own install script (https://abject.world/install)."""
    if os.name == "nt":
        # A PSModulePath inherited from PowerShell 7 hides Windows PowerShell's own modules (Get-FileHash), which the installer uses.
        env = {k: v for k, v in os.environ.items() if k.upper() != "PSMODULEPATH"}
        script = subprocess.run(["powershell.exe", "-NoProfile", "-Command", "irm https://abject.world/install.ps1"],
                                check=True, capture_output=True, text=True, env=env).stdout
        subprocess.run(["powershell.exe", "-NoProfile", "-Command", script], check=True, env=env)
    else:
        script = subprocess.run(["curl", "-fsSL", "https://abject.world/install.sh"], check=True, capture_output=True, text=True).stdout
        subprocess.run(["sh"], input=script, text=True, check=True)


def launch(app_path):
    target = Path(app_path).resolve()
    command = [shutil.which("abject") or "abject", "--data-dir", str(target)]
    if sys.platform == "darwin":
        from tokenbuffet.platforms.macos.terminal import launch as launch_terminal
        launch_terminal(command, target)
        return
    if os.name != "nt":
        raise ValueError(f"Open a terminal and run: {' '.join(command)}")
    subprocess.Popen(["powershell.exe", "-NoLogo", "-NoExit", "-Command", *command],
                     cwd=target, creationflags=subprocess.CREATE_NEW_CONSOLE)


def init(app_path=None):
    """Point the instance's own data directory at the router: Ollama URL, one router tier per Abject tier, and the permission mode."""
    check()
    folder = Path(__file__).resolve().parent
    config = json.loads((folder / "app_config.json").read_text(encoding="utf-8"))
    target = Path(app_path) if app_path else Path(config.get("path") or ".")
    if not target.is_absolute():
        target = (Path.cwd() if app_path else folder) / target
    target.mkdir(parents=True, exist_ok=True)
    client = config["client_settings"]
    settings = {"ai.credentials.ollama": client["active_endpoint"].removesuffix("/").removesuffix("/v1")}
    for tier, router_tier in client["task_model_tiers"].items():
        settings[f"ai.tiers.{tier}"] = f"ollama {router_tier}"
    settings["permissions.mode"] = client["permissions_mode"]
    abject = [shutil.which("abject"), "--data-dir", str(target)]
    subprocess.run([*abject, "start"], check=True)
    try:
        for path, value in settings.items():
            subprocess.run([*abject, "settings", "set", path, *value.split()], check=True)
    finally:
        subprocess.run([*abject, "stop"], check=True)
