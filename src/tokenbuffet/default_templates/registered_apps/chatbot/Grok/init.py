#!/usr/bin/env python3
"""Apply a chatbot instance's local router settings and workspace launcher."""

import fnmatch
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


def _launch_spec(app_path):
    target = Path(app_path).resolve()
    spec_file = target / "launch.json"
    if not target.is_dir() or not spec_file.is_file():
        raise FileNotFoundError(f"Chatbot launch settings not found: {spec_file}. Reapply this client's configuration from the Hub.")
    spec = json.loads(spec_file.read_text(encoding="utf-8"))
    if not (target / spec["requires"]).is_file():
        raise FileNotFoundError(f"Chatbot router settings missing: {target / spec['requires']}. Reapply this client's configuration from the Hub.")
    return target, spec


def prepare_demo(app_path):
    _launch_spec(app_path)


def launch(app_path):
    target, spec = _launch_spec(app_path)
    if sys.platform == "darwin":
        from tokenbuffet.platforms.macos.terminal import launch as launch_terminal
        expand = lambda value: value.replace("{workspace}", str(target))
        launch_terminal(list(map(expand, spec["command"])), target,
                        {key: expand(value) for key, value in spec["env"].items()})
        return
    if os.name != "nt":
        raise ValueError(f"Open this chatbot manually from {target} on this system")
    expand = lambda value: value.replace("{workspace}", str(target))
    executable = shutil.which(spec["command"][0])
    if not executable:
        raise FileNotFoundError(f"{spec['command'][0]} must be installed and available on PATH")
    env = {**os.environ, **{key: expand(value) for key, value in spec["env"].items()}}
    subprocess.Popen([executable, *map(expand, spec["command"][1:])], cwd=target, env=env,
                     creationflags=subprocess.CREATE_NEW_CONSOLE)


def _merge(existing, updates):
    for key, value in updates.items():
        if isinstance(value, dict) and isinstance(existing.get(key), dict):
            _merge(existing[key], value)
        else:
            existing[key] = value
    return existing


def _render(value, client):
    if isinstance(value, dict):
        return {key: _render(item, client) for key, item in value.items()}
    if isinstance(value, list):
        return [_render(item, client) for item in value]
    if isinstance(value, str):
        for key in ("active_endpoint", "single_model_tier"):
            value = value.replace("{" + key + "}", client[key])
    return value


def _write(root, relative, settings):
    target = (root / relative).resolve()
    if not target.is_relative_to(root):
        raise ValueError(f"Chatbot settings must stay inside the workspace: {relative}")
    target.parent.mkdir(parents=True, exist_ok=True)
    if settings["format"] == "json":
        existing = json.loads(target.read_text(encoding="utf-8")) if target.exists() else {}
        if not isinstance(existing, dict):
            raise ValueError(f"Expected JSON object in {target}")
        content = json.dumps(_merge(existing, settings["data"]), indent=2,
                             ensure_ascii=False) + "\n"
    elif settings["format"] == "text":
        content = settings["content"]
    else:
        raise ValueError("Unsupported chatbot settings format")
    target.write_text(content, encoding="utf-8")


def _copy_home(root, spec):
    """Copy the CLI's global home into the workspace home so its login carries over; never overwrites."""
    source = Path((spec.get("env") and os.environ.get(spec["env"])) or spec["default"]).expanduser()
    if not source.is_dir():
        print(f"No global {spec['default']} found; log in to the CLI once inside this workspace.")
        return
    target = (root / spec["to"]).resolve()
    if not target.is_relative_to(root):
        raise ValueError(f"Chatbot home must stay inside the workspace: {spec['to']}")
    print("Initializing chatbot workspaces...")
    for folder, dirs, files in os.walk(source):
        dirs[:] = [d for d in dirs if not any(fnmatch.fnmatch(d, pattern) for pattern in spec["skip"])]
        destination = target / Path(folder).relative_to(source)
        destination.mkdir(parents=True, exist_ok=True)
        for name in files:
            if not (destination / name).exists() and not any(fnmatch.fnmatch(name, pattern) for pattern in spec["skip"]):
                shutil.copy2(Path(folder) / name, destination / name)


def init(app_path=None):
    folder = Path(__file__).resolve().parent
    config = json.loads((folder / "app_config.json").read_text(encoding="utf-8"))
    settings = json.loads((folder / "app_settings.json").read_text(encoding="utf-8"))
    root = Path(app_path or config["path"])
    if not root.is_absolute():
        root = (folder / root).resolve()
    root = root.resolve()
    settings = _render(settings, config["client_settings"])
    _write(root, config["bridge_configuration"], settings)
    for relative, spec in settings["files"].items():
        _write(root, relative, spec)
    if "copy_home" in settings:
        _copy_home(root, settings["copy_home"])
