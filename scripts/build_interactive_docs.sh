#!/usr/bin/env bash
# Regenerate the interactive documentation site (site/) from docs/interactive-documentation/.
#
# Needs: pip install concept-mapmaker. Everything in the output folder is replaced.
# Arguments pass through to build_interactive_docs.py: [SRC] [--out OUT].
#
# Usage:
#   ./scripts/build_interactive_docs.sh
set -euo pipefail

python "$(dirname "$0")/build_interactive_docs.py" "$@"
