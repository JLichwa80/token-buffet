import json
import logging
from pathlib import Path


class ColorFormatter(logging.Formatter):
    _COLORS = {logging.WARNING: "\033[33m", logging.ERROR: "\033[31m", logging.CRITICAL: "\033[31m"}

    def format(self, record):
        text = super().format(record)
        color = self._COLORS.get(record.levelno)
        return f"{color}{text}\033[0m" if color else text


def console_handler(stream, fmt, datefmt="%H:%M:%S"):
    """A StreamHandler that colorizes WARNING+ by level when the stream is a TTY."""
    handler = logging.StreamHandler(stream)
    color = getattr(stream, "isatty", lambda: False)()
    handler.setFormatter((ColorFormatter if color else logging.Formatter)(fmt, datefmt=datefmt))
    return handler


def resolve_log_level(override=None, debug=False):
    if debug:
        return "DEBUG"
    if override:
        level = override.upper()
    else:
        path = Path.cwd() / "config" / "logging.json"
        level = json.loads(path.read_text(encoding="utf-8")).get("level", "INFO").upper() if path.exists() else "INFO"
    if level not in ("INFO", "DEBUG"):
        raise ValueError(f"Invalid logging level {level!r}; expected INFO or DEBUG")
    return level
