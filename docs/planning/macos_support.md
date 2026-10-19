# macOS support

Status: implementation prepared; no macOS run has been completed yet.

## Design

Keep one Token Buffet distribution and the shared proxy/router/dashboard. Put
macOS-specific behavior in `src/tokenbuffet/platforms/macos/`. Shared call sites
import this package only when `sys.platform == "darwin"`. Existing Windows
branches, provider templates, and Windows dependency requirements are preserved.

The adapter provides:

- `processes.py`: verify service command lines and stop their process trees with
  psutil, avoiding the Linux `/proc` assumption on macOS. The dependency is required
  only on macOS, through a packaging environment marker.
- `terminal.py`: launch provider login, chatbot workspaces, and Claudia through
  Apple Terminal. Pass the shell command as an AppleScript argument, with quoted
  paths/arguments and explicit session environment overrides. Command lookup uses
  Token Buffet's PATH, which is also passed to the Terminal session.
- `paths.py`: interpret configured home paths with either separator on macOS.
  The Windows Grok authentication setting is unchanged.

The existing POSIX/pexpect extractor remains shared. App-type launchers and their
matching bundled demo registrations include the same macOS-only delegation.
Existing installs must be recreated in a fresh workspace, as required by CLAUDE.md.

## Validation without owning a Mac

`.github/workflows/macos.yml` runs Python 3.12 on Apple Silicon (`macos-15`) and
Intel (`macos-15-intel`) GitHub-hosted runners. It runs on pushes to the
`macos-support` branch and supports manual dispatch once present on the default
branch. No provider credentials or subscription accounts are needed.

The workflow builds and installs a wheel, checks dependencies and packaged
templates, then invokes `scripts/ci/macos_smoke.py`. This verifies a fresh
workspace, actual PTY input/output and quota parsing using a synthetic CLI, model
extraction, router-to-proxy HTTP completion, dashboard stop actions, CLI shutdown,
and rejection of an unrelated PID. It also exercises launcher shell quoting with
spaces, apostrophes and Unicode, and compiles the AppleScript against the installed
Terminal dictionary. Logs and the dictionary are uploaded as artifacts, including
when runtime validation fails.

Passing these checks establishes the covered runtime behavior. It does not prove
vendor CLI login, real quota-screen compatibility, Terminal's visible interactive
launch, macOS Automation permissions, native folder selection, Keychain-based
credentials, or Obsidian demo initialization. Those require a real desktop session
and the relevant installed/logged-in applications. No complete macOS-support claim
should be made before those checks.

## Commands to run from Windows

Run in the repository's PowerShell terminal. These stage only the macOS changes,
leaving unrelated Obsidian workspace edits out of the commit.

```powershell
git switch -c macos-support
git add -- .gitignore .github/workflows/macos.yml scripts/ci/macos_smoke.py docs/planning/macos_support.md docs/README.md pyproject.toml src/tokenbuffet/platforms src/tokenbuffet/cli.py src/tokenbuffet/cli_proxy_server.py src/tokenbuffet/dashboard/server.py src/tokenbuffet/default_templates/integrations/chatbot/init.py src/tokenbuffet/default_templates/integrations/claudia/init.py src/tokenbuffet/default_templates/registered_apps/chatbot/Claude/init.py src/tokenbuffet/default_templates/registered_apps/chatbot/Gemini/init.py src/tokenbuffet/default_templates/registered_apps/chatbot/Grok/init.py src/tokenbuffet/default_templates/registered_apps/chatbot/OpenAI/init.py "src/tokenbuffet/default_templates/registered_apps/claudia/My Client Relationships Management/init.py"
git diff --cached --stat
git commit -m "Add isolated macOS support and validation workflow"
git push -u origin macos-support
gh run list --branch macos-support --limit 5
```

The push starts the workflow on the feature branch, so the workflow need not be
merged before its first validation. Use the run ID from the last command:

```powershell
gh run watch RUN_ID --exit-status
gh run view RUN_ID --log-failed
gh run download RUN_ID --dir ../tokenbuffet-macos-results
```

Only after validation and review, create and squash-merge the PR:

```powershell
gh pr create --base master --head macos-support --title "Add macOS support" --body "Add isolated macOS adapters and Apple Silicon/Intel runtime validation. Desktop and authenticated provider validation remain pending."
gh pr merge macos-support --squash
git switch master
git pull --ff-only
```

After the workflow is on `master`, manual reruns are also available:

```powershell
gh workflow run macos.yml --ref master
gh run list --workflow macos.yml --limit 5
```

## Setup on a Mac, when desktop access is available

Install Python 3.12+ and the desired vendor CLIs using their official setup guides.
Log into each CLI normally first. The commands below assume `python3.12` is on
PATH, and clone the validated feature branch rather than installing from PyPI:

```bash
git clone --branch macos-support https://github.com/JLichwa80/token-buffet.git
cd token-buffet
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install .
mkdir -p "$HOME/TokenBuffet-Mac"
cd "$HOME/TokenBuffet-Mac"
tbuffet init
tbuffet doctor
tbuffet start
```

Open `http://127.0.0.1:8080` or the dashboard URL printed during startup. Verify a
real provider's usage/models and an AI response, login terminal opening, chatbot
and Claudia workspace opening with the correct cwd/settings, native folder
selection, and provider/router stopping. Ctrl+C ends the foreground session.
Obsidian checks additionally require an installed/opened Obsidian and its enabled
CLI; then use `tbuffet demo init` and `tbuffet open obsidian conference-notes`.

## References

- [GitHub runner labels and private-repository usage](https://docs.github.com/en/actions/reference/runners/github-hosted-runners)
- [Manual workflows and the default-branch requirement](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow)
- [psutil process API](https://psutil.readthedocs.io/stable/)
- [Apple Terminal scripting and its dictionary](https://support.apple.com/guide/terminal/trml1003/mac)
