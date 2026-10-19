"""Driver for TUI CLIs, using a real pseudo-console (ConPTY via pywinpty on
Windows, a Unix pty via pexpect on macOS/Linux — see `_spawn_proc`).

Two problems make scraping a full-screen TUI non-trivial, both solved here:

1. Input delivery. A TUI reads keystrokes from the *console input buffer*, not
   piped stdin, so plain pipes (subprocess / pexpect.PopenSpawn) render the UI
   but never deliver input. winpty gives us a real PTY so keystrokes land.

2. Screen reconstruction. A TUI paints with cursor-move escapes, not newlines,
   so concatenating the raw stream loses all 2D layout. We feed the raw stream
   through `pyte` (a terminal emulator) to rebuild a clean line-based grid, and
   snapshot that grid after each tabbed view.

This module only *captures* the screen text; regex extraction lives in
`usage.parse_usage`, which runs over the captured/cleaned text. Config keys
(provider `usage` block): cli_cmd, command, views, tab_switch, gates, and the
optional timing/size knobs boot_wait, view_wait, submit_wait, cols, rows.
"""
import os
import shutil
import threading
import time

# NOTE: the capture-only deps (`pyte`, plus the platform PTY backend —
# `pywinpty` on Windows, `pexpect` on posix) are imported lazily inside the
# spawn helpers below, never at module top. pywinpty/pexpect are each
# single-platform; keeping the import lazy means the cross-platform `parse`
# path — which imports this module via `tokenbuffet.extractors.__main__` but never calls
# `drive_tui` — runs anywhere without any capture package installed.


def _resolve_cmd(argv):
    """Resolve argv[0] on PATH and wrap non-executable shims for the PTY.

    Configs name CLIs by bare command (`grok`, `claude`, `codex`), assuming the
    tool is installed and on PATH. A real pseudo-console can only launch an
    executable, so a `.cmd`/`.bat` shim (how npm installs claude/codex on
    Windows) is run via `cmd.exe /c`. The OS-specific launch detail stays here;
    the rest of the pipeline never sees a full path.
    """
    if not argv:
        return argv
    exe, rest = argv[0], list(argv[1:])
    resolved = shutil.which(exe) or exe
    ext = os.path.splitext(resolved)[1].lower()
    if os.name == 'nt' and ext in ('.cmd', '.bat'):
        return ['cmd.exe', '/c', resolved, *rest]
    return [resolved, *rest]


def _spawn_proc(cmd, rows, cols):
    """Spawn `cmd` in a real pseudo-console; return a process exposing
    read(size) / write(str) / terminate(force=).

    The one OS-specific seam in the capture path. Each backend lives in its own
    module — `_pty_windows` (ConPTY via pywinpty) and `_pty_posix` (Unix pty via
    pexpect) — imported lazily here so the platform PTY dependency loads only
    when capturing on that platform, and never on the `parse` path. Both return
    the same str-in/str-out surface, so `_spawn_and_collect` is OS-agnostic.
    """
    if os.name == 'nt':
        from . import _pty_windows as backend
    else:
        from . import _pty_posix as backend
    return backend.spawn(cmd, rows, cols)


def _spawn_and_collect(cmd, command_str, views, tab_switch,
                       boot_wait, view_wait, cols, rows, gates, submit_wait):
    """Launch the TUI, clear gates, run the command, snapshot each view.

    A background thread drains the PTY continuously (the TUI redraws/animates,
    so reads never stall). The main thread paces keystrokes and, at each view,
    feeds everything seen so far into a pyte screen and snapshots the grid.
    Returns the concatenated text of all snapshots.
    """
    import pyte                        # capture-only dep, imported lazily so
                                       # the `parse` path stays import-clean
    proc = _spawn_proc(cmd, rows, cols)
    chunks = []
    stop = threading.Event()

    def reader():
        while not stop.is_set():
            try:
                data = proc.read(8192)
            except (EOFError, Exception):
                break
            if data:
                chunks.append(data)
            else:
                time.sleep(0.03)

    screen = pyte.Screen(cols, rows)
    stream = pyte.Stream(screen)
    fed = [0]  # how many chunks already fed into the emulator

    def snapshot():
        while fed[0] < len(chunks):
            stream.feed(chunks[fed[0]])
            fed[0] += 1
        return '\n'.join(screen.display)

    t = threading.Thread(target=reader, daemon=True)
    t.start()
    snapshots = []
    try:
        time.sleep(boot_wait)                       # welcome screen settles
        for gate in gates:                          # answer onboarding prompts
            if gate.get('when', '').lower() in snapshot().lower():
                proc.write(gate.get('send', ''))
                time.sleep(gate.get('wait', view_wait))
        if command_str:
            if submit_wait:                         # autocomplete popups (codex)
                proc.write(command_str)             # need the typed command to
                time.sleep(submit_wait)             # settle before Enter submits;
                proc.write('\r')                    # a combined write is swallowed
            else:
                proc.write(command_str + '\r')
            time.sleep(view_wait)
        snapshots.append(snapshot())                # first view
        for _ in range(max(0, views - 1)):
            proc.write(tab_switch)
            time.sleep(view_wait)
            snapshots.append(snapshot())            # each subsequent view
    finally:
        stop.set()
        try:
            proc.terminate(force=True)
        except Exception:
            pass

    return '\n'.join(snapshots)


def drive_tui(usage_cfg):
    """Capture the TUI usage screen as text (all tabbed views concatenated)."""
    cmd = usage_cfg.get('cli_cmd')
    if not cmd:
        cmd = usage_cfg.get('execution', {}).get('cmd_template', [])[:2]
    if not cmd:
        raise ValueError('tui usage requires `cli_cmd` (no launch command found)')
    cmd = _resolve_cmd(cmd)

    return _spawn_and_collect(
        cmd,
        command_str=usage_cfg.get('command', ''),
        views=usage_cfg.get('views', 1),
        tab_switch=usage_cfg.get('tab_switch', '\t'),
        boot_wait=usage_cfg.get('boot_wait', 7),
        view_wait=usage_cfg.get('view_wait', 2.5),
        cols=usage_cfg.get('cols', 200),
        rows=usage_cfg.get('rows', 50),
        gates=usage_cfg.get('gates', []),
        submit_wait=usage_cfg.get('submit_wait', 0),
    )
