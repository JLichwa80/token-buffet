"""Locate and load provider configs from the registry."""
import json
import os
from pathlib import Path

_REGISTRY = str(Path(__file__).resolve().parents[2] / 'registered_providers')


def registry_dir():
    return _REGISTRY


def load_config(provider_or_path):
    """Load a config by provider name or by an explicit path.

    A bare name resolves to registered_providers/<name>/config.json.
    """
    if os.path.sep in provider_or_path or provider_or_path.endswith('.json'):
        path = provider_or_path
    else:
        path = os.path.join(_REGISTRY, provider_or_path, 'config.json')
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_section(provider_or_path, section):
    """Return just the requested section ("usage" or "models").

    Accepts either a full provider config (with a top-level `section` key) or a
    JSON that is already the section itself.
    """
    cfg = load_config(provider_or_path)
    if isinstance(cfg, dict) and section in cfg:
        return cfg[section]
    return cfg
