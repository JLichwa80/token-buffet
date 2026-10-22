#!/usr/bin/env bash
# Run `tbuffet start-router` in this workspace.
cd "$(dirname "$0")/.."
PYTHONIOENCODING=utf-8 exec python3 -m tokenbuffet.cli start-router "$@"
