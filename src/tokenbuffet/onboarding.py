"""Provider and app onboarding helpers shared by CLI and dashboard.

Everything here operates on the current working directory — tbuffet always
runs from the directory it manages, so paths are plain relative paths.
"""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

PROVIDER_INTEGRATIONS = Path("integrations") / "providers"


def _provider_catalog() -> dict:
    """Built-in provider name -> CLI command, read from each integrations/providers/<name>/config.json."""
    catalog = {}
    for path in sorted(PROVIDER_INTEGRATIONS.glob("*/config.json")):
        cfg = json.loads(path.read_text(encoding="utf-8"))
        cmd = (cfg.get("usage") or {}).get("cli_cmd") or (cfg.get("execution") or {}).get("cmd_template") or [path.parent.name]
        catalog[path.parent.name] = cmd[0]
    return catalog


def known_providers() -> list:
    return list(_provider_catalog())


def provider_cli(name: str) -> str:
    return _provider_catalog().get(name, name)


def detect_providers() -> dict:
    """Built-in provider name -> resolved CLI path, or None when its CLI is not on PATH."""
    return {name: shutil.which(cli) for name, cli in _provider_catalog().items()}


def child_env() -> dict:
    """Environment for extractor subprocesses: UTF-8 I/O and this package importable from any cwd."""
    pkg_root = str(Path(__file__).resolve().parent.parent)
    existing = os.environ.get("PYTHONPATH", "")
    return dict(os.environ, PYTHONIOENCODING="utf-8",
                PYTHONPATH=pkg_root + (os.pathsep + existing if existing else ""))


def list_providers() -> list:
    """Return sorted list of configured provider names."""
    reg = Path("registered_providers")
    if not reg.exists():
        return []
    return [d.name for d in sorted(reg.iterdir()) if d.is_dir() and (d / "config.json").exists()]


def import_provider_config(name: str, from_path: str, overwrite: bool = False) -> dict:
    """Copy a config file into registered_providers/<name>/config.json.

    Returns {"success": True, "path": str} or raises FileNotFoundError/ValueError.
    """
    src = Path(from_path).expanduser().resolve()
    if not src.exists():
        raise FileNotFoundError(f"Config file not found: {src}")
    try:
        with open(src, encoding="utf-8") as f:
            config = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Invalid JSON in {src}: {exc}")
    if not isinstance(config, dict):
        raise ValueError("Config must be a JSON object")

    dest_dir = Path("registered_providers") / name
    dest_path = dest_dir / "config.json"

    if dest_path.exists() and not overwrite:
        raise FileExistsError(
            f"Provider '{name}' already configured at {dest_path}. "
            f"Pass --overwrite to replace."
        )
    dest_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest_path)
    return {"success": True, "path": str(dest_path)}


def add_known_provider(name: str, overwrite: bool = False) -> dict:
    """Register a built-in provider by copying integrations/providers/<name>/config.json.

    Returns {"success": True, "path": str} or raises ValueError/FileNotFoundError.
    """
    if name not in known_providers():
        raise ValueError(
            f"Unknown provider '{name}'. Known providers: {', '.join(known_providers())}. "
            f"For a custom provider, use: tbuffet add-provider {name} --from /path/to/config.json"
        )
    return import_provider_config(name, str(PROVIDER_INTEGRATIONS / name / "config.json"), overwrite=overwrite)


def validate_provider(name: str) -> dict:
    """Run capture+parse for a provider to confirm it's logged in and quota is readable.

    Returns {success, remaining_pct, models_count} on success,
    or {success: False, error, hint} on failure.
    """
    config_path = Path("registered_providers") / name / "config.json"
    if not config_path.exists():
        return {
            "success": False,
            "error": f"Provider '{name}' not configured",
            "hint": f"Run: tbuffet add-provider {name}",
        }

    cli_name = provider_cli(name)
    if not shutil.which(cli_name):
        return {
            "success": False,
            "error": f"CLI '{cli_name}' not found on PATH",
            "hint": (f"Install {name}'s CLI tool, ensure it's on PATH, "
                     f"then run: tbuffet add-provider {name}"),
        }

    # Run capture+parse via the extractor module (no shell script dependency).
    status_dir = Path("data") / "providers_status"
    raw_dir = status_dir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    for op in ("usage", "models"):
        raw_path = raw_dir / f"{name}_{op}_raw.txt"
        out_path = status_dir / f"{name}_{op}.json"

        capture_cmd = [sys.executable, "-m", "tokenbuffet.extractors",
                       "capture", op, str(config_path), str(raw_path)]
        try:
            result = subprocess.run(
                capture_cmd, capture_output=True, text=True, encoding="utf-8",
                errors="replace", timeout=120, env=child_env(),
            )
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": f"Capture timed out (120s) for {op}",
                "hint": "The provider CLI may be stalled. Open it manually and log in.",
            }
        if result.returncode != 0:
            err = (result.stderr or result.stdout or "").strip()[-400:]
            if "No module named" in err:
                return {"success": False, "error": f"Capture failed ({op}): {err}",
                        "hint": "Package import problem, not a login issue. Reinstall token-buffet."}
            hint = (
                f"The {name} CLI may not be logged in. "
                f"Open '{cli_name}' and complete login, then retry."
            )
            return {"success": False, "error": f"Capture failed ({op}): {err}", "hint": hint}

        parse_cmd = [sys.executable, "-m", "tokenbuffet.extractors",
                     "parse", op, str(config_path), str(raw_path), str(out_path),
                     "--provider", name]
        try:
            result = subprocess.run(
                parse_cmd, capture_output=True, text=True, encoding="utf-8",
                errors="replace", timeout=30, env=child_env(),
            )
        except subprocess.TimeoutExpired:
            return {"success": False, "error": f"Parse timed out for {op}", "hint": ""}
        if result.returncode != 0:
            err = (result.stderr or result.stdout or "").strip()[-400:]
            return {"success": False, "error": f"Parse failed ({op}): {err}", "hint": ""}

    # Read back the parsed output.
    remaining = None
    models_count = 0
    usage_path = status_dir / f"{name}_usage.json"
    models_path = status_dir / f"{name}_models.json"

    try:
        with open(usage_path, encoding="utf-8") as f:
            usage_data = json.load(f)
        limits = usage_data.get("usage", {}).get("limits") or {}
        values = [v.get("remaining_pct") for v in limits.values()
                  if isinstance(v, dict) and v.get("remaining_pct") is not None]
        if values:
            remaining = min(values)  # the most constraining period
    except (OSError, json.JSONDecodeError):
        pass

    try:
        with open(models_path, encoding="utf-8") as f:
            models_data = json.load(f)
        models_count = len(models_data.get("models", {}).get("available", []))
    except (OSError, json.JSONDecodeError):
        pass

    return {"success": True, "remaining_pct": remaining, "models_count": models_count}


def remove_provider(name: str) -> dict:
    """Remove a provider config directory."""
    provider_dir = Path("registered_providers") / name
    if not provider_dir.exists():
        raise FileNotFoundError(f"Provider '{name}' not found")
    shutil.rmtree(provider_dir)
    return {"success": True, "removed": name}


def _load_register():
    """Load this directory's own integrations/register.py."""
    import importlib.util
    path = Path("integrations") / "register.py"
    if not path.is_file():
        raise FileNotFoundError(f"{path} missing. Run: tbuffet init")
    spec = importlib.util.spec_from_file_location("tb_register", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def list_app_types() -> list:
    base = Path("integrations")
    if not base.exists():
        return []
    return sorted(d.name for d in base.iterdir()
                  if d.is_dir() and not d.name.startswith("_") and (d / "app_config.json").is_file())


def list_apps() -> list:
    base = Path("registered_apps")
    return sorted(f"{c.parent.parent.name}/{c.parent.name}" for c in base.glob("*/*/app_config.json"))


def _app_type_module(app_type: str, name: str = ""):
    """integrations/<type>/init.py, or the instance's own registered_apps/<type>/<name>/init.py, or None."""
    import importlib.util
    path = Path("registered_apps") / app_type / name / "init.py" if name else Path("integrations") / app_type / "init.py"
    if not path.is_file():
        return None
    spec = importlib.util.spec_from_file_location(f"tb_init_{app_type}_{name}".rstrip("_"), path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def can_open(app_type: str, name: str) -> bool:
    module = _app_type_module(app_type, name)
    return module is not None and hasattr(module, "launch")


def _run_app_action(app_type: str, name: str, action: str) -> str:
    """Call the type's check() then <action>(app_path) for a registered instance; returns the app path."""
    instance = Path("registered_apps") / app_type / name
    config_path = instance / "app_config.json"
    if not config_path.is_file():
        raise FileNotFoundError(f"App instance not found: {app_type}/{name} (see: tbuffet list-apps)")
    config = json.loads(config_path.read_text(encoding="utf-8"))
    app_path = Path(config.get("path") or instance)
    if not app_path.is_absolute():
        app_path = (instance / app_path).resolve()
    module = _app_type_module(app_type, name)
    if module is None or not hasattr(module, action):
        raise ValueError(f"'{app_type}/{name}' has no {action} action")
    if hasattr(module, "check"):
        module.check()
    getattr(module, action)(str(app_path))
    return str(app_path)


def open_app(app_type: str, name: str) -> str:
    """Open a registered app instance via its type's launch(app_path)."""
    return _run_app_action(app_type, name, "launch")


def can_link(app_type: str) -> bool:
    module = _app_type_module(app_type)
    return module is not None and hasattr(module, "link")


def link_app(app_type: str, name: str) -> str:
    """Make the app itself aware of the instance (e.g. add a vault to Obsidian's vault list)."""
    return _run_app_action(app_type, name, "link")


def prepare_demo(app_type: str, name: str):
    """Apply a demo instance's settings, then run its demo setup hook if it declares one."""
    reapply_app(app_type, name)
    module = _app_type_module(app_type, name)
    if module is not None and hasattr(module, "prepare_demo"):
        return _run_app_action(app_type, name, "prepare_demo")


def check_app_type(app_type: str):
    """None if the app type declares no check(); "" if it passes; else the error text."""
    module = _app_type_module(app_type)
    if module is None or not hasattr(module, "check"):
        return None
    try:
        module.check()
    except (OSError, ValueError) as exc:
        return str(exc)
    return ""


def preview_app(app_type: str, name: str, app_path: str = "", extras: dict = None) -> dict:
    """Where register() would write the bridge settings, and whether that overwrites a file."""
    return _load_register().preview(app_type, name, app_path, extras)


def add_app(app_type: str, name: str, app_path: str = "", extras: dict = None) -> dict:
    """Register an app instance via this directory's register.register()."""
    reg = _load_register()
    instance, target = reg.register(app_type, name, app_path, extras or {})
    return {"instance": str(instance), "target": str(target)}


def reapply_app(app_type: str, name: str) -> dict:
    reg = _load_register()
    instance = (Path("registered_apps") / app_type / name).resolve()
    if not (instance / "app_config.json").is_file():
        raise FileNotFoundError(f"App instance not found: {instance}")
    cwd = os.getcwd()
    try:
        os.chdir(instance)
        target = reg.apply(instance)
    finally:
        os.chdir(cwd)
    return {"instance": str(instance), "target": str(target)}
