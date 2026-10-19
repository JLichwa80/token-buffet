#!/usr/bin/env python3
import json
from pathlib import Path

def configure():
    folder = Path(__file__).resolve().parent
    config = json.loads((folder / "app_config.json").read_text(encoding="utf-8"))
    target = Path(config.get("path") or ".")
    if not target.is_absolute():
        target = folder / target
    target = target / config.get("bridge_configuration", ".obsidian/plugins/karpathywiki/data.json")
    data = json.loads(target.read_text(encoding="utf-8")) if target.exists() else {}
    data.update(json.loads((folder / "app_settings.json").read_text(encoding="utf-8")))
    presets = json.loads((folder / "vault_types.json").read_text(encoding="utf-8"))
    data.update(presets[config.get("vault_type", "default")])
    settings = config["client_settings"]
    data.update(provider="custom-responses", baseUrl=settings["active_endpoint"],
                model=settings["single_model_tier"],
                usePerTaskModels=str(settings["model_mode"]).lower() == "true")
    for task, tier in settings["task_model_tiers"].items():
        data[task + "Model"] = tier
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
