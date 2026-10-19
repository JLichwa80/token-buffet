"""Apply declarative subprocess environment settings from a provider config."""

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
