# Publish Checklist

Document ID: `PUB-001`

Open steps for releasing `token-buffet`. Releases are built and uploaded by `.github/workflows/publish.yml` when a GitHub release is published.

1. **owner** Add `[project.urls]` (Homepage, Repository, Issues) to `pyproject.toml` where the `TODO(release)` comment is.
2. Tag the release: `git tag v<version>` and push the tag (0.2.5 is untagged).
