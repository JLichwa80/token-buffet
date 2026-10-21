#!/usr/bin/env python3
import importlib.util
import json
import sys
from pathlib import Path

type, path, *name = sys.argv[1:]
root = Path(__file__).resolve().parent.parent
chatbot = root / "integrations" / "chatbot"
workspace = Path(path).resolve()

preset = chatbot / "presets" / type
config = json.loads((preset / "app_config.json").read_text(encoding="utf-8"))
settings = json.loads((preset / "app_settings.json").read_text(encoding="utf-8"))

spec = importlib.util.spec_from_file_location("init", chatbot / "init.py")
init = importlib.util.module_from_spec(spec)
spec.loader.exec_module(init)
settings = init._render(settings, config["client_settings"])
init._write(workspace, config["bridge_configuration"], settings)
for relative, file in settings["files"].items():
    init._write(workspace, relative, file)
if "copy_home" in settings:
    init._copy_home(workspace, settings["copy_home"])

record = root / "registered_apps" / "chatbot" / workspace.name
record.mkdir(parents=True)
(record / "app_config.json").write_text(json.dumps(
    {"name": name[0] if name else workspace.name, "path": str(workspace), "type": type}, indent=2), encoding="utf-8")
