#!/usr/bin/env bash
# Refresh ALL registered providers: export usage + models JSON for each.
#
# Loops over registered_providers/* and runs read-provider.sh for each,
# writing the structured JSON to data/providers_status/ (which the router and
# proxies read). This is the external refresher: the router never scrapes --
# run this (on a schedule, or by hand) to refresh the files.
#
#   ./scripts/providers/read-providers.sh                 # every provider, usage + models
#   ./scripts/providers/read-providers.sh --op usage      # every provider, usage only
#   ./scripts/providers/read-providers.sh --provider grok # just grok, usage + models
set -euo pipefail

DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR/../.."
mkdir -p logs/extractors
exec > >(tee -a "logs/extractors/refresh-$(date +%Y%m%d-%H%M%S)-$$.log") 2>&1

ONLY_PROVIDER=""
OP="all"
while [ $# -gt 0 ]; do
    case "$1" in
        --provider) ONLY_PROVIDER="${2:-}"; shift 2 ;;
        --op)       OP="${2:-all}"; shift 2 ;;
        *) echo "usage: $0 [--provider NAME] [--op all|usage|models]" >&2; exit 2 ;;
    esac
done

if [ "$OP" = "all" ]; then OPS=(usage models); else OPS=("$OP"); fi
failed=0

for d in registered_providers/*/; do
    [ -d "$d" ] || continue
    prov=$(basename "$d")
    [ -z "$ONLY_PROVIDER" ] || [ "$prov" = "$ONLY_PROVIDER" ] || continue
    for o in "${OPS[@]}"; do
        echo "[read-providers] $prov $o ..."
        bash "$DIR/read-provider.sh" "$o" "$prov" || { echo "[read-providers] $prov $o FAILED"; failed=1; }
    done
done
if [ "$failed" -ne 0 ]; then exit 1; fi
echo "[read-providers] done -> data/providers_status/"
