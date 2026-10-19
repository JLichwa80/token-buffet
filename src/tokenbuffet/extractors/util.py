"""Generic helpers shared by every extractor strategy.

Nothing here knows about a specific provider.
"""
import re

_ANSI_RE = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')


def strip_ansi(text):
    """Remove ANSI escape sequences from terminal output."""
    return _ANSI_RE.sub('', text)


# Box-drawing (U+2500–257F) and block elements (U+2580–259F): modal borders,
# separators, and progress bars. Never part of extracted values, and they
# otherwise bleed into regex captures (e.g. a trailing "│"). Map to spaces so
# line structure and token spacing are preserved.
_BOX_RE = re.compile('[─-▟]')


def strip_box(text):
    """Replace box-drawing / block glyphs with spaces."""
    return _BOX_RE.sub(' ', text)


# Decorative, non-informative glyphs seen in TUI panels: braille (spinner/logo
# art), geometric shapes (◆◇◈ bullets), the ❯ prompt, ✗ close, and arrows.
_DECOR_RE = re.compile('[⠀-⣿■-◿✗❯←-⇿�]')
_ALNUM_RE = re.compile(r'[A-Za-z0-9]')


def clean_screen(text, strip_terms=(), drop_lines=()):
    """Render a scraped screen as clean readable text.

    Drops box/decorative glyphs, collapses runs of whitespace, and removes
    blank and consecutive-duplicate lines (TUI redraws repeat chrome).
    `strip_terms` are literal substrings removed inline first (e.g. the launch
    directory the CLI echoes into its header). `drop_lines` are substrings
    that, if found anywhere in a line, drop the whole line (provider-declared
    noise such as a telemetry banner); matched case-insensitively.
    """
    text = _DECOR_RE.sub(' ', _BOX_RE.sub(' ', text))
    for term in strip_terms:
        if term:
            text = text.replace(term, ' ')
    drops = [d.lower() for d in drop_lines if d]
    lines, prev = [], None
    for raw in text.splitlines():
        line = re.sub(r'\s+', ' ', raw).strip()
        # Drop blanks, consecutive repeats, and punctuation-only noise.
        if not line or line == prev or not _ALNUM_RE.search(line):
            continue
        low = line.lower()
        if any(d in low for d in drops):
            continue
        lines.append(line)
        prev = line
    return '\n'.join(lines)


def get_path(obj, dotted):
    """Walk a nested dict/list by a dotted path, e.g. "catalog.config.models".

    Returns None if any segment is missing. List indices are supported when a
    segment is an integer (e.g. "items.0.id").
    """
    curr = obj
    for part in dotted.split('.'):
        if isinstance(curr, list):
            try:
                curr = curr[int(part)]
            except (ValueError, IndexError):
                return None
        elif isinstance(curr, dict):
            if part not in curr:
                return None
            curr = curr[part]
        else:
            return None
    return curr


def set_path(root, dotted, value):
    """Set a value in a nested dict, creating intermediate dicts as needed."""
    parts = dotted.split('.')
    curr = root
    for part in parts[:-1]:
        curr = curr.setdefault(part, {})
    curr[parts[-1]] = value
    return root


# Names a `calculation` expression is allowed to reference, beyond value/limit.
_SAFE_NAMES = {
    'float': float, 'int': int, 'str': str,
    'min': min, 'max': max, 'round': round, 'abs': abs,
}


def safe_calc(expr, value, limit=None):
    """Evaluate a config `calculation` string in a locked-down namespace.

    Only `value`, `limit`, and a small set of numeric builtins are exposed;
    `__builtins__` is stripped so arbitrary code cannot run.
    """
    namespace = dict(_SAFE_NAMES)
    namespace['value'] = value
    namespace['limit'] = limit
    return eval(expr, {'__builtins__': {}}, namespace)
