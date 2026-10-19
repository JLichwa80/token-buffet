# Publish Checklist

Document ID: `PUB-001`

Steps to release `token-buffet` to PyPI. Steps marked **owner** need a decision or credentials only the project owner has.

1. **owner** Create the public repository, then add `[project.urls]` (Homepage, Repository, Issues) to `pyproject.toml` where the `TODO(release)` comment is.
2. Confirm `LICENSE` matches `license = { text = "MIT" }` in `pyproject.toml`.
3. Bump `version` in `pyproject.toml` and `src/tokenbuffet/__init__.py` if it defines one.
4. Confirm `src/tokenbuffet/default_templates/` matches `registered_providers/` and `integrations/` for the four bundled providers and the app types.
5. Build: `python -m build` (produces `dist/*.whl` and `dist/*.tar.gz`).
6. In a clean venv: `pip install dist/*.whl`, then `tokenbuffet init`, `tokenbuffet list-providers`, `tokenbuffet doctor`, `tokenbuffet dashboard`. Confirm the dashboard loads its static files.
7. **owner** Upload to TestPyPI first: `twine upload --repository testpypi dist/*`, then install from it in a clean venv with `pip install token-buffet`.
8. **owner** Upload to PyPI: `twine upload dist/*`.
9. Tag the release: `git tag v<version>` and push the tag.
