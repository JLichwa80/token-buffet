#!/usr/bin/env python3
import base64
import json
import os
import shutil
import subprocess
from pathlib import Path


def check():
    if not shutil.which("claude"):
        raise FileNotFoundError("Claude Code must be installed and available on PATH to open Claudia")


def launch(app_path):
    check()
    target = Path(app_path).resolve()
    if not target.is_dir() or not (target / "CLAUDE.md").is_file():
        raise FileNotFoundError(f"Claudia workspace not found: {target}")
    if os.name != "nt":
        raise ValueError(f"Open a terminal in {target} and run claude on this system")
    executable = shutil.which("claude")
    command = ("Set-Location -LiteralPath '" + str(target).replace("'", "''") + "'\n"
               "& '" + executable.replace("'", "''") + "'")
    encoded = base64.b64encode(command.encode("utf-16le")).decode("ascii")
    subprocess.Popen(["powershell.exe", "-NoLogo", "-NoProfile", "-NoExit",
                      "-EncodedCommand", encoded], cwd=target,
                     creationflags=subprocess.CREATE_NEW_CONSOLE)


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
    env["ANTHROPIC_MODEL"] = client["single_model_tier"]
    data.update(settings)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
