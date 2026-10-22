#!/usr/bin/env bash
# Release token-buffet: set the version, commit, tag, and push. GitHub Actions publishes to PyPI.
#
# Sets the version in pyproject.toml and src/tokenbuffet/__init__.py, commits everything
# (git add -A), tags v<version>, and pushes the commit and tag. The tag push starts
# .github/workflows/publish.yml, which builds and uploads via PyPI trusted publishing.
# Safe to re-run with the same version: nothing to commit is skipped and an existing tag is reused.
#
# Usage:
#   ./scripts/release.sh 0.2.0
set -euo pipefail
cd "$(dirname "$0")/.."

new="${1:?usage: release.sh X.Y.Z}"
[[ "$new" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]] || { echo "Version must be X.Y.Z" >&2; exit 1; }
current="$(grep -m1 '^version = ' pyproject.toml | cut -d'"' -f2)"
[ -n "$current" ] || { echo "No version found in pyproject.toml" >&2; exit 1; }
echo "Version $current -> $new"

sed -E -i.bak "s/^version = \".*\"/version = \"$new\"/" pyproject.toml
sed -E -i.bak "s/^__version__ = .*/__version__ = '$new'/" src/tokenbuffet/__init__.py
rm -f pyproject.toml.bak src/tokenbuffet/__init__.py.bak

git add -A
git diff --cached --quiet || git commit -m "Release $new"
[ -n "$(git tag -l "v$new")" ] || git tag "v$new"
git push --follow-tags
echo "Pushed v$new. Watch the publish run under the repo's Actions tab."
