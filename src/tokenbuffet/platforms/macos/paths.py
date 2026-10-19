"""Interpret configured home-relative paths on macOS."""

from pathlib import Path


def expand_path(value):
    # Provider templates may spell paths with Windows separators.
    return str(Path(value.replace("\\", "/")).expanduser()) if value else ""
