#!/usr/bin/env bash
# Regenerate the documentation site (site/) from docs/interactive-documentation/ and docs/static-pages/.
#
# Needs: pip install "concept-mapmaker>=0.2.0". Everything in the output folder is replaced.
# Arguments pass through to build_interactive_docs.py: [SRC] [--out OUT].
#
# Usage:
#   ./scripts/build_interactive_docs.sh
set -euo pipefail

python "$(dirname "$0")/build_interactive_docs.py" "$@"
