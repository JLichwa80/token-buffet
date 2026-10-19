#!/usr/bin/env python3
import json
from pathlib import Path

def configure():
    app_config = json.loads(Path("app_config.json").read_text(encoding="utf-8"))
    settings_data = json.loads(Path("app_settings.json").read_text(encoding="utf-8"))
    app_location = Path(app_config["path"])
    
    # apply settings to the app's target
