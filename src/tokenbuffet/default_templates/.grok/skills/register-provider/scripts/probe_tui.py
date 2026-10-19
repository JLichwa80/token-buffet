#!/usr/bin/env python3
"""Interactive TUI probe for registering a new provider.

Discovery tool, not part of the shipped pipeline: it launches a CLI's
interactive TUI through a real pseudo-console (ConPTY via pywinpty), paces a
few keystrokes, and prints the reconstructed screen (pyte) so the model can SEE
what a provider's boot gate, slash-command menu, `/model` picker, and `/usage`
panel actually look like before writing `config.json`.

It mirrors llm_cli_extractors/tui.py's capture loop (background reader thread + pyte
grid snapshot) but is fully parameterized from the command line and dumps the
RAW grid (no clean_screen), because regexes are written against the cleaned
text produced later by the real `capture` primitive — here the goal is to read
layout and find anchor strings.

Examples (run from the repo root):

    # 1. See the boot screen (and any trust gate) for an unknown CLI
    python .claude/skills/register-provider/scripts/probe_tui.py --cli agy --boot-wait 10

    # 2. Reveal the slash-command menu to find the model/usage command names
    python .claude/skills/register-provider/scripts/probe_tui.py --cli agy \
        --gate-when "do you trust" --explore

    # 3. Open and snapshot a specific panel (autocomplete popup -> submit-wait)
    python .claude/skills/register-provider/scripts/probe_tui.py --cli agy \
        --gate-when "do you trust" --command /usage --submit-wait 1.5 --view-wait 6

Windows/Git Bash notes:
  * Prefix the invocation with MSYS_NO_PATHCONV=1 so a leading-slash command
    like /usage is NOT rewritten into a C:\\... path by Git Bash. Running from
    PowerShell avoids the issue entirely.
  * Output is forced to UTF-8; box/braille glyphs would otherwise crash the
    default cp1252 console.
"""
import argparse
import os
import shutil
import sys
import threading
import time

import pyte
from winpty import PtyProcess


def resolve_cmd(argv):
    """Resolve argv[0] on PATH; wrap .cmd/.bat shims via cmd.exe (see tui.py)."""
    exe = shutil.which(argv[0]) or argv[0]
    ext = os.path.splitext(exe)[1].lower()
    if os.name == 'nt' and ext in ('.cmd', '.bat'):
        return ['cmd.exe', '/c', exe, *argv[1:]]
    return [exe, *argv[1:]]


def unescape(s):
    """Turn a literal '\\r'/'\\x1b' from the shell into real control bytes."""
    return s.encode('utf-8').decode('unicode_escape') if s else s


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--cli', nargs='+', required=True,
                    help='launch argv, e.g. --cli agy  or  --cli grok --no-alt-screen')
    ap.add_argument('--boot-wait', type=float, default=10.0)
    ap.add_argument('--gate-when', default='',
                    help='if this text is on screen after boot, send --gate-send')
    ap.add_argument('--gate-send', default=r'\r', help=r'keys to clear the gate (default \r)')
    ap.add_argument('--gate-wait', type=float, default=4.0)
    ap.add_argument('--command', default='',
                    help='slash command to type (e.g. /usage). Prefix the shell '
                         'invocation with MSYS_NO_PATHCONV=1 on Git Bash.')
    ap.add_argument('--submit-wait', type=float, default=1.5,
                    help='pause between typing the command and pressing Enter; '
                         'needed for autocomplete-popup TUIs (0 = Enter attached)')
    ap.add_argument('--view-wait', type=float, default=5.0,
                    help='wait after Enter before snapshotting the panel')
    ap.add_argument('--dismiss-banner', action='store_true',
                    help='send ESC before typing the command (clears a notice banner)')
    ap.add_argument('--explore', action='store_true',
                    help='type "/" and snapshot the slash-command menu instead of --command')
    ap.add_argument('--tabs', type=int, default=0,
                    help='Tab presses after the command, snapshotting each extra view')
    ap.add_argument('--cols', type=int, default=200)
    ap.add_argument('--rows', type=int, default=50)
    args = ap.parse_args()

    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

    cmd = resolve_cmd(args.cli)
    proc = PtyProcess.spawn(cmd, dimensions=(args.rows, args.cols))
    chunks, stop = [], threading.Event()

    def reader():
        while not stop.is_set():
            try:
                data = proc.read(8192)
            except Exception:
                break
            if data:
                chunks.append(data)
            else:
                time.sleep(0.03)

    screen = pyte.Screen(args.cols, args.rows)
    stream = pyte.Stream(screen)
    fed = [0]

    def snapshot():
        while fed[0] < len(chunks):
            stream.feed(chunks[fed[0]])
            fed[0] += 1
        return '\n'.join(l.rstrip() for l in screen.display if l.strip())

    def show(label):
        print(f'\n===== {label} =====')
        print(snapshot())

    threading.Thread(target=reader, daemon=True).start()
    try:
        time.sleep(args.boot_wait)
        show(f'BOOT (+{args.boot_wait:g}s)')

        if args.gate_when and args.gate_when.lower() in snapshot().lower():
            proc.write(unescape(args.gate_send))
            time.sleep(args.gate_wait)
            show(f'AFTER GATE "{args.gate_when}"')

        if args.dismiss_banner:
            proc.write('\x1b')
            time.sleep(1.0)

        if args.explore:
            proc.write('/')
            time.sleep(2.5)
            show('SLASH MENU (type more to filter: see references/workflow.md)')
        elif args.command:
            proc.write(args.command)
            if args.submit_wait:
                time.sleep(args.submit_wait)
                proc.write('\r')
            else:
                proc.write('\r')
            time.sleep(args.view_wait)
            show(f'PANEL after "{args.command}"')
            for i in range(max(0, args.tabs)):
                proc.write('\t')
                time.sleep(args.view_wait)
                show(f'TAB VIEW {i + 1}')
    finally:
        stop.set()
        try:
            proc.terminate(force=True)
        except Exception:
            pass


if __name__ == '__main__':
    main()
