"""Windows capture backend: a real pseudo-console via ConPTY (pywinpty).

Imported only on Windows, and only lazily (by `tui._spawn_proc`), so the
Windows-only `winpty` dependency never loads on macOS/Linux or on the
cross-platform `parse` path. The posix counterpart is `_pty_posix`; both expose
the same `spawn(cmd, rows, cols)` surface so `tui` stays OS-agnostic.
"""
from winpty import PtyProcess


def spawn(cmd, rows, cols):
    """Spawn `cmd` in a ConPTY; return a process with read/write/terminate.

    pywinpty's PtyProcess already exposes `read(size) -> str`, `write(str)` and
    `terminate(force=)` — exactly the surface the capture loop needs — so it is
    returned directly with no adapter. `cmd` is already PATH-resolved (and any
    `.cmd`/`.bat` shim wrapped) by `tui._resolve_cmd`.
    """
    return PtyProcess.spawn(cmd, dimensions=(rows, cols))
