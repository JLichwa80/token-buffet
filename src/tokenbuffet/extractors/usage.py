"""Usage extraction from a captured TUI screen.

Consistent with models: the screen is captured elsewhere (TUI driver), and
parse_usage runs regexes over the resulting text to build a flat, intuitive
structured dict, e.g.:

    {
      "plan": "Claude Pro",
      "limits": {
        "session": {"used_pct": 73.0, "remaining_pct": 27.0, "resets": "9:40pm"},
        "weekly":  {"used_pct": 23.0, "remaining_pct": 77.0, "resets": "Oct 13, 11am"}
      },
      "gathered_at": "2026-10-07T20:30:00-07:00"
    }

A provider can expose one or several concurrent limits (grok shows a weekly
limit; claude shows a session *and* a weekly limit). Both are described the
same way: `periods` maps a period name to its `pct` / `resets` regexes (`pct`
captures whatever percentage the provider prints, used or left). A period whose
    `pct` regex doesn't match is reported as `null` (N/A), unless the period's
    optional `exhausted` pattern matches an explicit limit message — so a
declared-but-absent period (e.g. grok's daily) shows up explicitly without any
provider-specific code. Flat descriptive fields (plan, ...) come from
`extractors`. `remaining_pct` is canonical — the config's `calculation` maps the
provider's raw percentage to it (whether reported as used or left) — and
`used_pct` is derived as its complement.
"""
import re
from datetime import datetime

from .util import set_path, safe_calc

_FLAGS = re.DOTALL | re.IGNORECASE


def _to_number(s):
    """First numeric token in a string as a float (e.g. '80%' -> 80.0)."""
    if s is None:
        return None
    m = re.search(r'[\d.]+', str(s))
    return float(m.group()) if m else None


def _search(pattern, text):
    if not pattern:
        return None
    m = re.search(pattern, text, _FLAGS)
    return m.group(1).strip() if m else None


def _period_entry(spec, text, calc, limit):
    """One limit's {used_pct, remaining_pct, resets}, or None if not present.

    `remaining_pct` is canonical: the config's `calculation` maps the provider's
    raw on-screen percentage to it, whether the provider reports consumed (grok:
    "80%", calc `100 - value`) or remaining (codex: "100% left", calc `value`).
    `used_pct` is then derived as the complement, so the two always sum to 100.
    """
    if spec.get('exhausted') and re.search(spec['exhausted'], text, _FLAGS):
        entry = {'used_pct': 100.0, 'remaining_pct': 0.0}
        if 'resets' in spec:
            entry['resets'] = _search(spec.get('resets'), text)
        return entry
    raw = _search(spec.get('pct'), text)
    if raw is None:
        return None                              # declared period not on screen
    raw_num = _to_number(raw)
    remaining_pct, used_pct, calc_error = None, raw_num, None
    if raw_num is not None:
        if calc:
            try:
                remaining_pct = round(float(safe_calc(calc, raw, limit)), 2)
                used_pct = round(100 - remaining_pct, 2)
            except Exception as e:
                calc_error = f'{type(e).__name__}: {e}'
        else:
            remaining_pct = round(100 - raw_num, 2)   # no calc: raw is the used %
    entry = {'used_pct': used_pct, 'remaining_pct': remaining_pct}
    if 'resets' in spec:
        entry['resets'] = _search(spec.get('resets'), text)
    if calc_error:
        entry['calc_error'] = calc_error
    return entry


def parse_usage(cfg, text):
    """Extract a structured usage dict from captured text (cheap, re-runnable)."""
    if not cfg:
        return {'error': 'no usage config'}

    out = {}
    # Descriptive fields (plan, ...) pass through as-is.
    for key, pattern in (cfg.get('extractors') or {}).items():
        value = _search(pattern, text)
        if value is not None:
            set_path(out, key, value)

    calc = cfg.get('calculation')
    limit = cfg.get('limit')
    periods = cfg.get('periods') or {}
    if periods:
        out['limits'] = {name: _period_entry(spec, text, calc, limit)
                         for name, spec in periods.items()}

    out['gathered_at'] = datetime.now().astimezone().isoformat(timespec='seconds')
    return out
