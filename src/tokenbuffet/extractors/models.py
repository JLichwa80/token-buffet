"""Model-list extraction from captured text.

Consistent with usage: the text is captured elsewhere — either the TUI driver
(`tui`) or the non-interactive `models` subcommand (`subcmd`) — and this just
parses it. `list_regex` is applied per line to yield one entry per model.

Each entry is `{"id": ..., "name": ...}` where `id` is the identifier the CLI
accepts for `--model` and `name` is the human label. The regex supplies them
via named groups `(?P<id>...)` / `(?P<name>...)`; if it has only one capture
group, that group is used for both (the label *is* the id, e.g. codex). A line
containing `default_marker` (default "(default)") marks the default; `default`
is reported as that entry's `id`.

Optional `id_case` (`"lower"` or `"upper"`) normalizes the executable model id
while preserving the display name. `list_start` / `list_end` bound the scan to
the picker region: lines
are ignored until one contains `list_start`, and scanning stops at the first
line containing `list_end`. This keeps a provider's header/footer (which may
echo the current model) from leaking into the list. Both are matched
case-insensitively; omitting them scans the whole text.
"""
import re


def parse_models(cfg, text):
    """Return {"available": [{"id","name"}...], "default": <id|None>}."""
    if not cfg:
        return {'error': 'no models config'}
    pattern = cfg.get('list_regex')
    if not pattern:
        return {'error': 'models config needs `list_regex`'}

    rx = re.compile(pattern)
    marker = cfg.get('default_marker', '(default)')
    id_case = cfg.get('id_case')
    start = (cfg.get('list_start') or '').lower()
    end = (cfg.get('list_end') or '').lower()
    active = not start
    models, seen, default = [], set(), None
    for line in text.splitlines():
        low = line.lower()
        if not active:                              # skip until the list begins
            if start in low:
                active = True
            continue
        if end and end in low:                      # stop at the list's end
            break
        m = rx.search(line)
        if not m:
            continue
        gd = m.groupdict()
        if 'id' in gd:                              # explicit id/name groups
            mid = (gd.get('id') or '').strip()
            name = (gd.get('name') or mid).strip()
        else:                                       # single group: label is id
            mid = m.group(1).strip()
            name = mid
        if id_case == 'lower':
            mid = mid.lower()
        elif id_case == 'upper':
            mid = mid.upper()
        if not mid:
            continue
        if mid not in seen:
            seen.add(mid)
            models.append({'id': mid, 'name': name})
        if marker and marker in line:
            default = mid
    return {'available': models, 'default': default}
