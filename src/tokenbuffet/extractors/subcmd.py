"""Non-interactive extractor: run a CLI subcommand and capture its stdout.

The counterpart to `tui.drive_tui` for data the interactive TUI does not expose.
The `/model` picker shows a friendly label (`Grok 4 Fast`, `Gemini 3.1 Pro`) but
not the identifier the CLI accepts for `--model` (`grok-4.7-build-fast`,
`gemini-3.1-pro-high`). The CLIs' `models` subcommands print that mapping
non-interactively, so a provider opts in by declaring `list_cmd` in its `models`
config; `capture` then runs this instead of driving the TUI.

Unlike the TUI path this needs no pseudo-console or terminal emulator — the
output is plain line-oriented text — so it is pure stdlib and cross-platform
(no pyte / pywinpty / pexpect).
"""
import subprocess

from .tui import _resolve_cmd   # stdlib-only helper (PATH + .cmd/.bat shim)


def run_list_cmd(cfg):
    """Run `cfg['list_cmd']` non-interactively and return its combined output.

    stdin is closed (DEVNULL) so a CLI that would otherwise fall back to an
    interactive picker fails fast instead of hanging; stderr is folded into
    stdout because some CLIs print the listing (or a 'not logged in' notice)
    there. `list_timeout` (default 60s) bounds a hung fetch.
    """
    argv = cfg.get('list_cmd')
    if not argv:
        raise ValueError('non-interactive models requires `list_cmd`')
    argv = _resolve_cmd(list(argv))
    proc = subprocess.run(
        argv,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        timeout=cfg.get('list_timeout', 60),
    )
    return proc.stdout or ''
