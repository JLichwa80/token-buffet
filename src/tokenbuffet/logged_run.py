"""Run a Python module with console output also appended to a repository log."""
import argparse
import datetime
import re
import runpy
import sys
import traceback
from .log_paths import LOG_DIR

_ANSI = re.compile(r"\033\[[0-9;]*m")

class Tee:
    def __init__(self, console, log):
        self.console, self.log = console, log
    def write(self, text):
        self.log.write(_ANSI.sub("", text))
        self.log.flush()
        return self.console.write(text)
    def flush(self):
        self.log.flush()
        self.console.flush()
    def __getattr__(self, name):
        return getattr(self.console, name)

def main():
    parser = argparse.ArgumentParser(add_help=False, allow_abbrev=False)
    parser.add_argument("--log", required=True)
    parser.add_argument("--module", required=True)
    args, rest = parser.parse_known_args()
    log_name = args.log
    if args.module == "tokenbuffet.cli_proxy_server" and "--provider" in rest:
        provider = rest[rest.index("--provider") + 1]
        log_name = f"{provider}/proxy/console.log"
    path = LOG_DIR / log_name
    path.parent.mkdir(parents=True, exist_ok=True)
    stdout, stderr = sys.stdout, sys.stderr
    with path.open("a", encoding="utf-8") as log:
        sys.stdout, sys.stderr = Tee(stdout, log), Tee(stderr, log)
        code = 0
        try:
            print(f"[{datetime.datetime.now().isoformat()}] START {args.module}")
            sys.argv = [args.module, *rest]
            runpy.run_module(args.module, run_name="__main__")
        except SystemExit as exc:
            code = exc.code
            raise
        except KeyboardInterrupt:
            code = 130
        except BaseException as exc:
            code = 1
            traceback.print_exc(file=log)
            print(f"FAIL module={args.module} reason={' '.join(str(exc).split())[:500]}")
            raise SystemExit(1)
        finally:
            print(f"[{datetime.datetime.now().isoformat()}] EXIT {code}")
            sys.stdout, sys.stderr = stdout, stderr

if __name__ == "__main__":
    main()
