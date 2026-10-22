#!/usr/bin/env bash
# Run `tbuffet stop-provider` in this workspace [name] (omit for all providers).
cd "$(dirname "$0")/.."
PYTHONIOENCODING=utf-8 exec python3 -m tokenbuffet.cli stop-provider "$@"
