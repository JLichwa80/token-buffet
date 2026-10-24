#!/usr/bin/env bash
# Deploy token-buffet: commit, push and publish the GitHub Release for the version in pyproject.toml.
#
# Run ./scripts/release.sh X.Y.Z first to set the version. Publishing the GitHub Release starts
# .github/workflows/publish.yml, which builds and uploads via PyPI trusted publishing.
#
# Usage:
#   ./scripts/deploy.sh
set -euo pipefail
cd "$(dirname "$0")/.."

version="$(grep -m1 '^version = ' pyproject.toml | cut -d'"' -f2)"
[ -n "$version" ] || { echo "No version found in pyproject.toml" >&2; exit 1; }
echo "Deploying v$version"

git add -A
git commit -m "Release $version"
git push
gh release create "v$version" --title "v$version" --generate-notes
