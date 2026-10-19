#!/usr/bin/env python3
"""Register an app instance or reapply its bridge settings."""
import argparse
import importlib.util
import json
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
INTEGRATIONS = ROOT / "integrations"
INSTANCES = ROOT / "registered_apps"


PRESET_KEYS = ("presets_directory", "preset_label")


def _merge(base, updates):
    for key, value in updates.items():
        base[key] = _merge(base[key], value) if isinstance(value, dict) and isinstance(base.get(key), dict) else value
    return base


def _segment(value):
    if not value or value in (".", "..") or Path(value).name != value or "/" in value or "\\" in value:
        raise ValueError("App type and name must be single folder names")
    return value


def _module(path):
    spec = importlib.util.spec_from_file_location(path.stem + "_" + path.parent.name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _app_path(instance, config):
    app_path = Path(config.get("path") or instance)
    return app_path if app_path.is_absolute() else (instance / app_path).resolve()


def _target(instance, config):
    return _app_path(instance, config) / (config.get("bridge_configuration") or "app_settings.json")


def template(app, extras=None):
    source = INTEGRATIONS / _segment(app)
    base = json.loads((source / "app_config.json").read_text(encoding="utf-8"))
    preset = (extras or {}).get("preset")
    directory = base.get("presets_directory")
    if directory:
        choices = sorted(p.parent.name for p in (source / directory).glob("*/app_config.json"))
        if not preset or preset not in choices:
            raise ValueError(f"Choose --preset from: {', '.join(choices)}")
        source = source / directory / _segment(preset)
        reserved = [key for key in PRESET_KEYS if key in json.loads((source / "app_config.json").read_text(encoding="utf-8"))]
        if reserved:
            raise ValueError(f"Preset '{preset}' sets type-level keys: {', '.join(reserved)}")
        if not (source / "app_settings.json").is_file():
            raise FileNotFoundError(f"Preset settings missing: {source / 'app_settings.json'}")
    elif preset:
        raise ValueError(f"{app} does not define registration presets")
    return source


def preview(app, name, app_path="", extras=None):
    source, instance = validate(app, name, app_path, extras)
    config = json.loads((source / "app_config.json").read_text(encoding="utf-8"))
    config["path"] = str(Path(app_path).resolve()) if app_path else str(instance.resolve())
    if (extras or {}).get("bridge_configuration"):
        config["bridge_configuration"] = extras["bridge_configuration"]
    target = _target(instance, config)
    settings_path = source / "app_settings.json"
    settings = json.loads(settings_path.read_text(encoding="utf-8")) if settings_path.is_file() else {}
    paths = [target, *(_app_path(instance, config) / p for p in settings.get("files", {}))]
    return {"target": str(target), "exists": target.exists(), "instance_exists": False,
            "files": [{"target": str(p), "exists": p.exists()} for p in paths]}


def apply(instance):
    instance = Path(instance).resolve()
    config = json.loads((instance / "app_config.json").read_text(encoding="utf-8"))
    target = _target(instance, config)
    init = instance / "init.py"
    if init.exists():
        _module(init).init(str(_app_path(instance, config)))
    configure = instance / "configure.py"
    if configure.exists():
        _module(configure).configure()
    return target


def validate(app, name, app_path="", extras=None):
    """Raise on any input register() would reject; returns (source, instance)."""
    app, name = _segment(app), _segment(name)
    source = INTEGRATIONS / app
    if not (source / "app_config.json").is_file():
        raise ValueError(f"Unknown app type: {app}")
    instance = INSTANCES / app / name
    if instance.exists():
        raise FileExistsError(f"App instance already exists: {instance}")
    extras = extras or {}
    unknown = set(extras) - {"vault_type", "bridge_configuration", "label", "preset"}
    if unknown:
        raise ValueError("Unsupported registration fields: " + ", ".join(sorted(unknown)))
    source = template(app, extras)
    base = json.loads((source / "app_config.json").read_text(encoding="utf-8"))
    if base.get("path") == "[app_path]" and not app_path:
        raise ValueError(f"{app} apps need --path <app folder>")
    presets = source / "vault_types.json"
    if presets.is_file():
        known = json.loads(presets.read_text(encoding="utf-8"))
        vault_type = extras.get("vault_type") or "default"
        if vault_type not in known:
            raise ValueError(f"Unknown vault type '{vault_type}'. Choose: {', '.join(known)}")
    init = INTEGRATIONS / app / "init.py"
    if init.is_file():
        check = getattr(_module(init), "check", None)
        if check:
            check()
    return source, instance


def register(app, name, app_path="", extras=None):
    source, instance = validate(app, name, app_path, extras)
    extras = extras or {}
    instance.mkdir(parents=True)
    for layer in dict.fromkeys((INTEGRATIONS / app, source)):
        for file in layer.iterdir():
            if file.is_file():
                shutil.copy2(file, instance / file.name)
    config_path = instance / "app_config.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    if source != INTEGRATIONS / app:
        type_config = json.loads((INTEGRATIONS / app / "app_config.json").read_text(encoding="utf-8"))
        config = _merge({k: v for k, v in type_config.items() if k not in PRESET_KEYS}, config)
    config.update(name=name, path=str(Path(app_path).resolve()) if app_path else str(instance.resolve()))
    config.setdefault("type", app)
    if extras.get("preset"):
        config["preset"] = extras["preset"]
    if (source / "vault_types.json").is_file():
        config["vault_type"] = extras.get("vault_type") or "default"
    if extras.get("label"):
        config["label"] = extras["label"]
    if extras.get("bridge_configuration"):
        config["bridge_configuration"] = extras["bridge_configuration"]
    config_path.write_text(json.dumps(config, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return instance, apply(instance)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("app", help="registered integration type")
    parser.add_argument("name", help="new or existing instance name")
    parser.add_argument("app_path", nargs="?", default="", help="application folder; defaults to instance folder")
    parser.add_argument("extras", nargs="*", help="preset=..., vault_type=... or bridge_configuration=...")
    parser.add_argument("--reapply", action="store_true", help="apply existing instance settings")
    args = parser.parse_args()
    if "=" in args.app_path:
        args.extras.insert(0, args.app_path)
        args.app_path = ""
    extras = dict(extra.split("=", 1) for extra in args.extras)
    if args.reapply:
        instance = INSTANCES / _segment(args.app) / _segment(args.name)
        if not (instance / "app_config.json").is_file():
            raise FileNotFoundError(instance)
        target = apply(instance)
    else:
        instance, target = register(args.app, args.name, args.app_path, extras)
    print(json.dumps({"instance": str(instance), "bridge_configuration": str(target)}))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError) as exc:
        sys.exit(f"Error: {exc}")
