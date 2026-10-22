#!/usr/bin/env bash
# Run `tbuffet stop-router` in this workspace.
cd "$(dirname "$0")/.."
PYTHONIOENCODING=utf-8 exec python3 -m tokenbuffet.cli stop-router "$@"
