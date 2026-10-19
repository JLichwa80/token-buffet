"""Posix (macOS/Linux) capture backend: a Unix pty via pexpect.

Imported only off-Windows, and only lazily (by `tui._spawn_proc`), mirroring
the Windows backend `_pty_windows`. Both expose `spawn(cmd, rows, cols)`
returning a process with `read(size) -> str`, `write(str)` and
`terminate(force=)`, so the shared pyte reconstruction in `tui` is identical on
every platform.
"""
import pexpect


class _Proc:
    """Adapt a pexpect child to pywinpty's PtyProcess surface (str in/out)."""

    def __init__(self, child):
        self._child = child

    def read(self, size):
        try:
            return self._child.read_nonblocking(size, timeout=0.1)
        except pexpect.TIMEOUT:
            return ''              # no data yet; caller idle-sleeps
        except pexpect.EOF:
            raise EOFError         # process exited; stop the reader thread

    def write(self, data):
        self._child.send(data)

    def terminate(self, force=False):
        try:
            self._child.terminate(force=force)
        except Exception:
            pass


def spawn(cmd, rows, cols):
    """Spawn `cmd` in a Unix pty; return the read/write/terminate adapter.

    `cmd` is already PATH-resolved by `tui._resolve_cmd` (argv[0] is the program,
    the rest are args). encoding='utf-8' makes reads return str — pexpect's
    incremental decoder handles control sequences split across reads — and
    echo=False keeps typed slash-commands / gate answers out of the stream.
    """
    child = pexpect.spawn(cmd[0], args=list(cmd[1:]), dimensions=(rows, cols),
                          encoding='utf-8', codec_errors='replace', echo=False)
    return _Proc(child)
