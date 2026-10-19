"""Launch a CLI in Apple's Terminal with explicit cwd and session environment.

Apple documents Terminal scripting and osascript here:
https://support.apple.com/guide/terminal/trml1003/mac
Terminal's installed scripting dictionary defines the `do script` command.
"""

import os
from pathlib import Path
import shlex
import shutil
import subprocess


APPLESCRIPT = '''on run argv
    tell application "Terminal"
        do script (item 1 of argv)
        activate
    end tell
end run
'''


def shell_command(command, cwd, env=None):
    """Quote argv and only the session overrides, keeping values out of AppleScript."""
    target = Path(cwd).resolve(strict=True)
    if not target.is_dir():
        raise NotADirectoryError(target)
    if not command:
        raise ValueError("No terminal command supplied")
    executable = shutil.which(command[0])
    if not executable:
        raise FileNotFoundError(f"{command[0]} must be installed and available on PATH")
    environment = {"PATH": os.environ["PATH"], **(env or {})}
    for key, value in environment.items():
        if not key or not key.isascii() or not (key[0].isalpha() or key[0] == "_") or not all(c.isalnum() or c == "_" for c in key):
            raise ValueError(f"Invalid environment variable: {key}")
        if "\0" in value:
            raise ValueError(f"Invalid environment value: {key}")
    invocation = ["/usr/bin/env", *(f"{key}={value}" for key, value in environment.items()),
                  executable, *command[1:]]
    return f"cd {shlex.quote(str(target))} && {shlex.join(invocation)}"


def launch(command, cwd, env=None):
    """Open Terminal; a rejected Automation request is reported as an error."""
    shell = shell_command(command, cwd, env)
    # Pass command text as argv, rather than interpolating it into AppleScript.
    result = subprocess.run(["/usr/bin/osascript", "-", shell], input=APPLESCRIPT,
                            capture_output=True, text=True, timeout=30)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or "Terminal could not open the CLI")
