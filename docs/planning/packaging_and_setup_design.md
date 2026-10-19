# Packaging & Setup Design — install + first-run UX

> **Dependencies superseded (2026-10-17):** there are no optional extras. Every dependency (`pyte`, `pywinpty`/`pexpect`, `openai`, `ai`) is required, Python 3.12+, and the install is `pip install token-buffet`. The `[capture]`/`[responses]`/`[uistream]`/`[all]` sections and missing-dependency hints below are historical.

Document ID: `PKG-001` · Status: **approved** (Phase A complete; Phase B unblocked). All decisions
locked — see summary at the end. Each section states the current state, the options considered, and
the **locked decision** with rationale.

## Product name — **Token Buffet** (locked)

All-you-can-eat AI from the flat-rate subscriptions you already pay for.

| Thing | Name |
|---|---|
| Product / brand | Token Buffet |
| PyPI dist | `token-buffet` |
| CLI command | `tokenbuffet` |
| CLI alias | `tbuffet` |
| Workspace dir | `~/.tokenbuffet` |
| Core Python package | `tokenbuffet` |
| Extractor subsystem | `tokenbuffet.extractors` |
| Dashboard package | `tokenbuffet.dashboard` |

Current codebase names (`tbuffet`, `tokenbuffet`, `tokenbuffet.extractors`, `tokenbuffet.dashboard`) are
the rename targets in T08-I1.

---

## 0. Who this is for, and the promise

**User:** a non-AI, moderately-technical person — comfortable installing a Python CLI, not comfortable
hand-authoring a TUI-scraping JSON config. (The "regular person" from
[consumer_routing_roadmap.md](../integrations/consumer_routing_roadmap.md) arrives later, through the dashboard.)

**Promise:** `pipx install tbuffet` → `tbuffet setup` → their Claude/Codex/Grok/agy
subscriptions are now a local OpenAI/Ollama/Anthropic/Gemini-compatible API, and their apps are wired
to it — **without** the AI `register-provider` skill and **without** editing JSON.

### The happy path we are designing toward

```text
$ pipx install "tbuffet[capture]"
$ tbuffet setup
  → Scaffolds a workspace at ~/.tbuffet (first run).
  → Detects installed provider CLIs:  claude ✓   codex ✓   grok ✗ (not found)   agy ✗
  → For each detected provider: "Log in now? [Y/n]" → launches the vendor CLI's login,
    then captures /usage + /model to confirm it works.      claude ✓ 88% · 42 models
  → "Add an app? [Obsidian vault / Chatbot client / skip]" → guided add-app.
  → Runs doctor: workspace ✓  claude ✓  codex ✓  ports free ✓  capture deps ✓
$ tbuffet start           # proxies + router(8090) + dashboard(8080)
$ tbuffet status          # live port/PID/quota per layer
```

Everything `setup` does is also available as discrete commands (D5) and as dashboard actions (D6), so
CLI, scripted, and GUI users land in the same place.

---

## D1. Installation & distribution

**Current:** `pyproject.toml` → name `token-buffet`, v0.1.0, `dependencies = []`, console scripts
`tokenbuffet` + `tbuffet`, packages `tokenbuffet*`,
`requires-python >=3.8`. Package-data references `tokenbuffet/default_templates/**` (which does not
exist — see D2) and `tokenbuffet.dashboard/static/**`.

**Dependency story — options:**

| Option | What | Trade-off |
|--------|------|-----------|
| A. All-as-hard-deps | `pyte`, `pywinpty`/`pexpect`, `openai`, `ai_sdk` always installed | Kills the "stdlib-only core" property; forces a C-extension (`pywinpty`) on everyone |
| B. **Zero-dep core + extras** | bare install = stdlib only; opt into features | Preserves the core ethos; user must pick an extra for capture |

**Recommended: B.** Declare extras with environment markers:
- `[capture]` → `pyte` + `pywinpty; sys_platform=='win32'` + `pexpect; sys_platform!='win32'`
  — needed to onboard/refresh any provider (scrape `/usage` + `/model`).
- `[responses]` → `openai` — only the `/v1/responses` path needs it.
- `[uistream]` → the `ai.ui.ai_sdk` UI-message stream — **open question:** this import is not a
  standard PyPI package today; it may need vendoring or stay an advanced, manual extra (flagged below).
- `[all]` → everything installable.

Because onboarding requires capture, the **documented default install is
`pipx install "tbuffet[capture]"`**; the bare `tbuffet` stays dependency-free for
runtime/parse-only use.

**Distribution:** recommend **pipx** as the primary install (it's a standalone CLI app → isolated venv,
no dependency clashes); plain `pip install` still works. Polish PyPI metadata (license, project URLs,
keywords, long-description from README). Build with `python -m build`; publish via `twine` or PyPI
Trusted Publishing from CI. Start at semver 0.1.x.

**Python floor:** audit shows walrus (`:=`, 3.8) is the newest syntax used; keep **`>=3.8`**.

**Locked:** extras layout as above. `[uistream]` → `pip install ai` (Vercel AI SDK for Python, public beta); note in docs it requires Python 3.12+. Core package floor stays lower. `pipx` is the documented default install.

---

## D2. Workspace scaffolding

**Current:** everything is **cwd-relative** (`registered_providers/`, `config/`, `data/`, `logs/` under
the directory you run from). `init` makes those dirs and copies `default_templates/` — but **that
template dir does not ship**, so a fresh install's `init` creates empty dirs and copies nothing.

**Workspace location — options:**

| Option | Behavior | Trade-off |
|--------|----------|-----------|
| A. cwd (today) | state lives wherever you run | must `cd` to the same dir every time; surprising for a global CLI |
| B. **Default home workspace** | `~/.tbuffet` (or OS app-dir), overridable by `--workspace` / `CLI_LLM_BRIDGE_HOME` | one obvious location; needs a single path-resolver refactor since code assumes cwd |

**Recommended: B** — a default workspace root resolved once at startup
(`CLI_LLM_BRIDGE_HOME` env > `--workspace` flag > `~/.tbuffet`; if the cwd already looks
initialized, prefer it for back-comat). All modules read paths from that resolved root instead of
`os.getcwd()`. This is the single biggest internal change and is called out as an implementation cost
(T08-I1/I4).

**Bundled defaults:** create a real package-data template tree (e.g. `tokenbuffet/default_templates/`)
carrying the four vetted `registered_providers/{claude,codex,grok,agy}/config.json`, the
`template_config.json`, a seed `config/router_config.json`, and the `integrations/` app-type files
(`_base`, `obsidian`, `chatbot`, `claudia` + `register.py`). Fix `pyproject` package-data to point at
it. `init` copies these so a fresh install is immediately populated — the four known providers present
but **inactive until logged in** (D3).

**Locked:** `~/.tokenbuffet` as default workspace (`TOKENBUFFET_HOME` env > `--workspace` flag > `~/.tokenbuffet`). Ship all 4 provider configs as bundled recipes. **Superseded (2026-10-17):** there is no workspace resolution. tbuffet always runs in the current directory, with relative paths.

---

## D3. Provider onboarding UX — the hard part

**Current:** authoring a provider config means driving its TUI with the AI **`register-provider`
skill**. A plain pip user can't do that.

**Key insight:** the config is the hard, AI-authored artifact — and for the four known providers we
**already have vetted configs**. So for them, onboarding is *not* authoring; it is:
1. **Detect** the CLI on `PATH` (e.g. `claude`, `codex`, `grok`, the agy binary).
2. **Log in** — launch the vendor CLI's own interactive login; we cannot and should not automate vendor
   auth. Honest and simple.
3. **Validate** — run `capture` + `parse` for `/usage` and `/model`. A successful usage capture *is* the
   login check (an unauthenticated TUI stops at its login gate, which the capture will surface), so
   step 2 and step 3 share one mechanism.
4. **Enable** — mark the provider active; it now participates in routing.

**Flows (recommended):**
- **`tbuffet setup`** — the first-run wizard: lists the four known providers with detected/not-
  found status, offers to log in + validate each, reports `provider ✓ NN% · M models` or a concrete
  failure, and (optionally) chains into app onboarding (D4).
- **`tbuffet add-provider <name>`** — do one provider; `--from <config.json>` imports a
  hand- or AI-authored config for a provider we don't ship.
- **New/unshipped providers** keep the **AI `register-provider` skill** as the documented "author a new
  provider config" path, feeding `add-provider --from`. A non-AI generic TUI-prober wizard is a
  stretch goal, not required for v1.

**Capture deps:** if `[capture]` isn't installed, `setup`/`add-provider` detect the missing import and
tell the user to `pipx inject tbuffet pyte pexpect` (or reinstall with `[capture]`), rather than
failing cryptically.

**Locked:** validate-by-capture doubles as the login check. AI skill (`register-provider`) is the
authoring path for any provider — vetted or new. `tbuffet add-provider --from <config.json>` imports
the AI-authored config. No non-AI generic prober for v1.

---

## D4. App onboarding UX

**Current:** `python integrations/register.py <app> <name> [path] [extras]` run from `integrations/`.
It copies the app-type files into `registered_apps/<app>/<name>/`, writes `app_config.json`, backs up
the target to `.bak`, and runs the instance's `init.py` + `configure.py`. App types present: `obsidian`,
`chatbot`, `claudia`.

**Recommended:** wrap it as **`tbuffet add-app <type> <name> [--path ...] [--vault-type ...]`**
calling `register.register()` directly (no `cd`, no second code path). Interactive wizard:
- discovers app types from the bundled/`integrations/` tree,
- prompts for the app's folder (defaulting to the instance folder),
- **shows the exact target file it will write and a preview/diff, backs it up to `.bak`, then confirms
  before writing** (dry-run-by-default + confirm),
- plus `list-apps` and `reconfigure-app <type> <name>` (the existing `--reapply`).

**Locked:** dry-run-preview-then-confirm as the default write behavior for app settings.

---

## D5. CLI command surface

**Recommended subcommands** (argparse, one `tbuffet`):

| Command | Does |
|---------|------|
| `init` | scaffold the workspace + copy bundled defaults (idempotent) |
| `setup` | first-run wizard: providers (D3) → optional apps (D4) → doctor |
| `add-provider` / `list-providers` / `remove-provider` | per-provider lifecycle; `--from` import |
| `add-app` / `list-apps` / `reconfigure-app` / `remove-app` | per-app lifecycle (D4) |
| `start` [`--detach`] / `stop` / `restart` / `status` | fleet lifecycle (D7) |
| `doctor` | preflight checks (D8) |
| `dashboard` | launch the GUI (8080) |

**CLI-first** for `setup`/`add-provider`/`add-app` (scriptable, SSH/headless-friendly); the dashboard
(D6) is the friendly GUI mirror of the same operations. `setup` is the guided umbrella that most users
run once.

**Locked:** command names as above (with `tokenbuffet` / alias `tbuffet`). `read-provider.*` shell
scripts replaced by `tbuffet` subcommands; `.ps1`/`.sh` scripts removed.

---

## D6. Dashboard as setup hub

**Current:** `src/tokenbuffet.dashboard/` serves status/config/logs (and has control endpoints).

**Recommended:** the dashboard mirrors the CLI onboarding — **Add Provider** (detect → launch login →
validate), **Add App** wizard, router-mode/`custom_order` edit, and start/stop — with both the CLI and
the GUI calling **one shared module** so they can't diverge. The GUI is the path for the non-technical
audience; the CLI is the power/headless path. Keep the server stdlib-only.

**Build order:** CLI-first in Phase B; the GUI mirror lands after the CLI flows exist (T08-I5 after
I2/I3), so the shared module is proven before the GUI wraps it.

**Locked:** GUI is the primary path for most users; CLI is for power/headless users. Both call one
shared module. GUI onboarding (T08-I5) built after CLI flows (T08-I2/I3) are proven.

---

## D7. Cross-platform & process lifecycle

**Current:** a sprawl of `scripts/*.ps1` / `*.sh` (`start_bridge`, `start_router`, `start_dashboard`,
`stop_all`, …) plus `scripts/providers/read-provider[s].*`. `tbuffet start` blocks the terminal
and waits on children; there is no `stop`/`status` in the CLI.

**Recommended:**
- Fold fleet control into cross-platform **`start`/`stop`/`restart`/`status`** subcommands. `start`
  writes a PID+port registry (the existing `data/providers_status/<p>_run_status.json` already carries
  live port/PID/status); `stop`/`status` read it. Offer **`start --background`** with a
  foreground default.
- **Port conflicts:** `start` and `doctor` check 8001.. / 8090 / 8080 and error with the offender and a
  fix, instead of a bind traceback.
- **Capture PTY:** ConPTY (Windows) / pty (POSIX) are already chosen lazily; `doctor` verifies the
  correct `[capture]` dep for the running platform.
- Keep the `.ps1`/`.sh` as thin shims that call the CLI (back-compat), or deprecate them in docs.

**Locked (updated 2026-10-18):** `start` and `restart` run in the foreground by default;
Ctrl+C stops the session's process trees. Use `--background` to leave services running.
Shell scripts removed; replaced by
`tbuffet` subcommands. PID+port registry via existing `_run_status.json`.

---

## D8. Doctor / preflight / troubleshooting UX

**Current:** each proxy now exits with a visible, specific error if its startup usage-capture fails
(recent change), but there is no aggregate "is my setup healthy?" check.

**Recommended:** **`tbuffet doctor`** checks, each failure printing one concrete fix:
- workspace initialized & writable;
- for each registered provider: CLI on `PATH`, logged in (cached `run_status` or a quick capture);
- `[capture]` deps importable for this platform; `[responses]`/`[uistream]` present iff those wire
  paths are in use;
- ports 8001.. / 8090 / 8080 free;
- router config valid (tiers resolve to real model ids).

Run `doctor` automatically at the end of `init` and `setup` so the first thing a user sees is a green
checklist or an actionable red line.

**Locked:** checklist confirmed. `doctor` runs automatically at the end of `setup`.

---

## Locked decisions (Phase A complete)

| # | Decision |
|---|---|
| D1 | **Install:** `pipx install "token-buffet[capture]"` documented default; zero-dep core; extras `[capture]` / `[responses]` / `[uistream]` (→ `ai`, requires Python 3.12+) / `[all]` |
| D2 | **Workspace:** `~/.tokenbuffet` default (`TOKENBUFFET_HOME` env > `--workspace` > `~/.tokenbuffet`); 4 provider configs bundled as shipped recipes. **Superseded (2026-10-17):** there is no workspace resolution. tbuffet always runs in the current directory, with relative paths. |
| D3 | **Provider onboarding:** AI skill authors any config; `tbuffet add-provider --from <config.json>` imports it; validate-by-capture = login check |
| D4 | **App onboarding:** `tbuffet add-app` wraps `register.register()`; dry-run preview + confirm before write |
| D5 | **CLI surface:** `tokenbuffet` / alias `tbuffet`; subcommands `init` / `setup` / `add-provider` / `add-app` / `start` / `stop` / `status` / `doctor` / `dashboard`; `.ps1`/`.sh` scripts removed |
| D6 | **Dashboard:** GUI is primary path for most users; CLI for power/headless; both share one module; GUI onboarding after CLI flows proven |
| D7 | **Process model:** `start`/`restart` foreground by default, `--background` opt-in; Ctrl+C stops the session's process trees |
| D8 | **Doctor:** checklist confirmed; runs automatically at end of `setup` |
