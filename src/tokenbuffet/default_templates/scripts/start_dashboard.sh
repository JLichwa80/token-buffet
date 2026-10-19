#!/usr/bin/env bash
# Back-compat shim: use `tbuffet dashboard` directly.
cd "$(dirname "$0")/.."
PYTHONIOENCODING=utf-8 exec python -m tokenbuffet.cli dashboard "$@"
