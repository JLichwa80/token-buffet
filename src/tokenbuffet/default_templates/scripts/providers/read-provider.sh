#!/usr/bin/env bash
# Read a provider's usage/quota or model list out of its CLI (macOS/Linux entry point).
#
# These numbers only exist on the vendor CLI's interactive /usage and /model
# screens -- there is no API for them. This drives the real CLI through a pty,
# reads what it prints, and turns it into JSON:
#   usage   -> remaining quota per period (how much is left before you hit a limit)
#   models  -> the models that provider currently offers
#
# Two steps run under the hood: capture (drive the TUI, clean the screen into
# tests/<provider>_<op>_raw.txt) then parse (regexes over that text into
# tests/<provider>_<op>.json). Python provides only those two primitives
# (python -m tokenbuffet.logged_run --log extractors/console.log --module tokenbuffet.extractors capture|parse).
#
# Usage:
#   ./scripts/providers/read-provider.sh <op> <config> [--raw-only] [--extract <file.txt>]
#     <op>      usage  -> how much quota is left   |   models -> model list
#     <config>  provider name, config.json path, or section JSON
set -euo pipefail

DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$DIR/../.." && pwd)"          # repo root (parent of scripts/providers/)
STATUS_DIR="$ROOT/data/providers_status"  # structured JSON the router/proxy read
RAW_DIR="$STATUS_DIR/raw"                 # captured screen text (for regex iteration)
mkdir -p "$RAW_DIR" "$STATUS_DIR"
# Make the extractor module importable regardless of the caller's cwd.
export PYTHONPATH="$ROOT/src:$ROOT:${PYTHONPATH:-}"
PYTHON="${PYTHON:-python3}"

usage() {
  echo "usage: $0 <models|usage> <config> [--raw-only] [--extract FILE]" >&2
  exit 2
}

[ $# -ge 2 ] || usage
OP="$1"; CONFIG="$2"; shift 2
case "$OP" in models|usage) ;; *) usage ;; esac

RAW_ONLY=0
EXTRACT=""
while [ $# -gt 0 ]; do
  case "$1" in
    --raw-only) RAW_ONLY=1; shift ;;
    --extract)  EXTRACT="${2:-}"; shift 2 ;;
    *) usage ;;
  esac
done

name_for() {
  local inp="${1%/}"; inp="${inp%\\}"
  local base; base="$(basename "$inp")"
  if [ "$base" = "config.json" ] || [ "$base" = "config" ]; then
    local parent; parent="$(basename "$(dirname "$inp")")"
    [ -n "$parent" ] && echo "$parent" || echo provider
  else
    local n="${base%.json}"
    [ -n "$n" ] && echo "$n" || echo provider
  fi
}

NAME="$(name_for "$CONFIG")"
RAW_PATH="$RAW_DIR/${NAME}_${OP}_raw.txt"
JSON_PATH="$STATUS_DIR/${NAME}_${OP}.json"

# Resolve a bare provider name to its repo-root config.json; leave explicit paths untouched.
CONFIG_PATH="$CONFIG"
case "$CONFIG" in
  */*|*\\*|*.json) ;;
  *) CONFIG_PATH="$ROOT/registered_providers/$CONFIG/config.json" ;;
esac

if [ -n "$EXTRACT" ]; then
  # Extraction only, from the given capture file.
  exec "$PYTHON" -m tokenbuffet.logged_run --log extractors/console.log --module tokenbuffet.extractors parse "$OP" "$CONFIG_PATH" "$EXTRACT" "$JSON_PATH" --provider "$NAME"
fi

"$PYTHON" -m tokenbuffet.logged_run --log extractors/console.log --module tokenbuffet.extractors capture "$OP" "$CONFIG_PATH" "$RAW_PATH"

if [ "$RAW_ONLY" -eq 1 ]; then
  echo "raw-only: saved $RAW_PATH" >&2
  exit 0
fi

exec "$PYTHON" -m tokenbuffet.logged_run --log extractors/console.log --module tokenbuffet.extractors parse "$OP" "$CONFIG_PATH" "$RAW_PATH" "$JSON_PATH" --provider "$NAME"
