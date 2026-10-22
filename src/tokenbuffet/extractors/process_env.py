"""Apply declarative subprocess environment settings from a provider config."""

import json
import os
from pathlib import Path


_REPO = Path(__file__).resolve().parents[2]


def build_process_env(config, base=None):
    """Return an environment for a provider CLI, creating declared directories."""
    env = dict(os.environ if base is None else base)
    settings = config.get("process_env", {})
    for key in settings.get("unset", []):
        env.pop(key, None)
    values = {key: str(value).replace("{repo}", str(_REPO))
              for key, value in settings.get("set", {}).items()}
    for path in settings.get("mkdir", []):
        Path(str(path).replace("{repo}", str(_REPO))).mkdir(parents=True, exist_ok=True)
    env.update(values)
    return env


def isolated_home(config):
    """Return (home dir, env var names) for a config's execution.isolated_home, or None."""
    spec = config.get("execution", {}).get("isolated_home")
    if not spec:
        return None
    return Path(spec["path"].replace("{workspace}", str(Path.cwd()))), spec["env"]


def prepare_isolated_home(config):
    """Write the JSON files an execution.isolated_home declares, overwriting existing ones."""
    found = isolated_home(config)
    if not found:
        return None
    home, _ = found
    for relative, data in config["execution"]["isolated_home"]["files"].items():
        target = home / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return home
