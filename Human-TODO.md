# Human TODO

Manual checks for `TODO.md`. Run them yourself with live CLIs and a browser. Start the fleet from the repository root with `python -m tokenbuffet.cli start` unless a step says otherwise. Record each client's version, request path, selected backend and model, and any failure in `docs/chatbots.md`. For a failure, save the HTTP status, response body or stream error, and the request field names after removing secrets and prompt content.


## Finish

- [ ] T05: For each of the four chatbots, confirm a short prompt and a normal local tool task finish without a protocol error or recursive CLI launch. Put the versions, paths, selected models, and any failures in `docs/chatbots.md`.

## Release (T08-I6) — owner-only

- [ ] T08-I6: Create the public GitHub repo and add `[project.urls]` to `pyproject.toml`; confirm the `LICENSE` is correct. Then follow `docs/planning/publish_checklist.md`: build the wheel, `twine upload`, and tag the release. (Already done: README quick-start, wheel build + clean-venv install verified, workspace-based `log_paths`, keywords/classifiers.)
