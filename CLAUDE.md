# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Rules

Do not run tests unless the user explicitly instructs you to run them. Inspect code and logs without running test commands by default.

**This is the first MVP (pilot) build — nothing has been released and there are no existing users or installs to preserve.** Never add backward-compatibility code, migration paths, version checks, fallbacks for older file layouts, or "if the old file lacks X" shims. When something changes, change it everywhere and delete the old code. A test install that is out of date is deleted and re-created with `tbuffet init`, not upgraded in place.

All local services (proxies, router, dashboard) bind to and are addressed at **`127.0.0.1`**, never `localhost` — use `src/tokenbuffet/loopback.py` (`HOST`, `serve`, `listening`, `url`) rather than writing the address by hand. App configs, demo settings and docs that point at our ports use `127.0.0.1` too.

Only the user does git writes. Never run `git add`, `git commit`, `git push`, `git reset`, `git rm`, `git stash`, `git merge`, `git rebase`, or any other command that modifies the git history or staging area. Read-only git commands (`git status`, `git log`, `git diff`, `git show`) are fine.

Avoid multiple paths, fallbacks - Fail Fast instead vs swallowing issues, exceptions

**KISS — do exactly what was asked, nothing invented.** Build the simplest thing that satisfies the request. Don't add fields, ids, naming schemes, validation, safeguards, options, helpers or files nobody asked for. If the request leaves a design choice open, ask one short question instead of inventing an answer, and when the user states the model (e.g. "path and name, nothing else"), implement that model literally.

**Nothing extra unless asked.** Do only what was asked. Do not add behavior, launches, fallbacks, messages, hints, tests, or fixes for neighbouring problems, and do not edit anything outside this repo (user profiles, global config, installed apps), unless the user asks for it. If something else looks broken, report it in one line and leave it. "Run X" means run X, not edit code. If an instruction is clear, do it; do not explain why it is already fine.

**A delete command deletes — fully, immediately.** This is the user's personal machine and Claude's sandbox; nothing on it is shared or valuable. "Delete X" / "reset X" means remove all of X (e.g. all of `~/.claudia`, not only the demo folders), with no confirmation question first, no backup-first step, no "this is shared / are you sure" caveats, and no leaving part of it in place to report afterwards. Stop any process holding it, delete, then report in one line.

**Never guess how an external app or CLI behaves, and never build on a guess.** Every behavior a feature, guard, refusal or workaround depends on must be either documented in that app's latest public documentation (looked up now, and cite the page) or tested live. Undocumented, untested behavior doesn't go into code or into explanations as fact: say it's unverified and ask. (Example: "Obsidian overwrites `obsidian.json` on close" was a guess, false, and the guard built on it was removed.)

**Never remove an integration capability** because nothing uses it yet. Every chat option / wire format (OpenAI chat and text completions, Ollama chat/generate, OpenAI Responses, Anthropic Messages, Gemini GenerateContent, `--ui-stream` Vercel AI SDK UI-message stream), and tool-call handoff stay — each one lets more apps integrate. The "delete old code" rule above applies to backward-compat code and dead legacy code, not to these. If keeping one has a cost (e.g. `ai` requires Python 3.12+), state the cost and keep the capability.

## What this is

   "f89c9ae567b42e0a": {
            "path": "G:\\My Drive\\QuickNotes",
            "ts": 1791676913890
        }

A pure-Python proxy + router that exposes **CLI-based LLMs** (Claude, Codex, Grok, agy/antigravity, …) as a standard **OpenAI / Ollama / Anthropic / Gemini-compatible HTTP API**. Downstream apps (e.g. the Obsidian LLM Wiki plugin, or another CLI agent pointed at the router as a gateway) talk HTTP; the proxy shells out to each vendor's interactive CLI under the hood.

The whole system is **config-driven**: adding or changing a provider means editing a declarative `registered_providers/<name>/config.json` — the Python engine has no provider-specific branches. Preserve this. A change that only works for one provider belongs in that provider's config, not in the engine.

## Architecture — three long-running processes

`tbuffet start` launches one process per layer, each wrapped by `tokenbuffet.logged_run` so its console goes to `logs/` (see `src/tokenbuffet/cli.py:start_fleet`):

1. **Proxy** (`cli_proxy_server.py`), one per provider, port from `config.json → server.port` (claude 8001, etc.). Receives chat requests, flattens `messages` into a text prompt, spawns the provider CLI per `execution.cmd_template` (`{prompt_file}` → a temp file, `{prompt}` → the prompt inline as an arg; the model id is appended via `execution.model_arg`'s `{model}`, and a request's `effort`/`reasoning_effort` — when present — via `execution.effort_arg`'s `{effort}`, all verbatim — no per-provider rewriting), and parses the CLI's stream-json stdout back into chat chunks using `stream.text_extractors` (`matches` selects a JSON line, `path` pulls the token — `[]` means "join over a list"). The wire format is keyed on the **request path** — each native envelope by default, `--ui-stream true` instead emits the Vercel `ai.ui.ai_sdk` UI-message SSE for the OpenAI/Ollama paths (opt-in output format):
   - `/v1/chat/completions`, `/api/chat` — OpenAI chat
   - `/v1/completions` — OpenAI text; `/api/generate` — Ollama
   - `/v1/responses` (+ `/v1/chat/responses`) — OpenAI **Responses** API, built through the `openai` SDK's Pydantic event types
   - `/v1/messages` — text-only **Anthropic Messages** SSE (`anthropic_sse.py`)
   - `/v1(beta)/models/{model}:generateContent` / `:streamGenerateContent` — text-only **Gemini** GenerateContent (`gemini_wire.py`)

   On startup each proxy **binds its port first** (the next free port if the configured one is taken by a foreign process), publishes it to `data/providers_status/<provider>_run_status.json`, then reads its own usage and models **in a background thread**, retrying every 300s on failure and refreshing every `--refresh-interval`. The status file carries `usage: {state: reading|ready|unavailable, reason}`, which the dashboard shows. Its GET endpoints `/usage`, `/models`, `/v1/models`, `/api/tags` answer from the last saved export while a capture is running and return 503 "still being read" when there is none. If `execution.sandbox.enabled`, each request runs the CLI in a fresh temp dir with the auth file copied in and pointed at via the configured `env_var` (e.g. grok's `GROK_HOME`), torn down after.

2. **Router** (`local_router.py`), fleet and direct-launch port **8090** (Ollama-compatible). Maps a **semantic tier** (`fast`/`medium`/`reasoning`) to provider backends via its own **`config/router_config.json`**, **populated once per provider**: as soon as a running proxy's models are readable and that provider has no entry yet, the router resolves its tier **regex** (`config.json → tiers`, matched case-insensitively) against the model ids returned by each **running proxy's `/models` endpoint** to the **newest matching id** (first in file order, since CLIs list newest-first), then writes a frozen snapshot of exact `{provider, model}` ids per tier, stamping each with a default **effort** (`fast`→`low`, `medium`→`medium`, `reasoning`→`high`). Delete the file (or clear `tiers`) to repopulate; otherwise exact ids are used verbatim and hand-edits win — there is **no per-request regex resolution**. `router_config.json → mode`: **`usage`** load-balances by remaining quota (routes a tier to the backend with the most left, skipping depleted `<=0` or not-running backends); **`custom`** ignores quota and routes by the global **`custom_order`** provider preference list. On forward the router injects `payload["effort"]`, resolved by precedence: request `effort`/`reasoning_effort` > per-backend effort > the provider's `effort` map > the global `effort` map > the tier default (all keyed by tier in `router_config.json`). It forwards to the live port each proxy published to `_run_status.json`. A request naming a provider (`"claude"`) instead of a tier resolves to that provider's first tier.

   **Client apps and CLI agents** (Claude Code, Codex, Grok, agy) point at the router root like they would at Ollama — `http://127.0.0.1:8090` (plus `/v1` for OpenAI-style clients); there is no per-client route. Requests carrying client tools get one structured tool-call decision from a backend CLI (`tool_wire.py`); the **client**, not the bridge, executes the tool and supplies the result on the next request. Provider configs may add `execution.tool_handoff_args` (e.g. claude/grok use `--tools ""`) for such requests. Responses-API continuation history (`previous_response_id`) is held in router memory (~100 recent, lost on restart). See `docs/integrations/chatbots.md`.

3. **Dashboard** (`dashboard/server.py`, static UI in `dashboard/static/`), port **8080** — HTML status + configuration view built from exported quota, model, process, and request/log files.
   Tabs are real URLs (`TAB_PATHS` in `app.js`, mirrored as `STATIC_FILES` routes in `server.py` — add both when adding a tab): Home `/`, My Apps `/my-apps`, My Chatbots `/my-chatbots`, LLM Providers `/llm-providers`, advanced-only `/router` and `/activity`. The URL is the only tab state (no `localStorage` tab). My Apps and My Chatbots share one renderer (`APP_KINDS` in `app.js`; `isChatbot()` splits the two lists, also used by Home). Connect buttons are generated, not hard-coded: one per app type, or per CLI preset for preset-registered types (the chatbot type), labelled from each preset's own `app_config.json` `name` (served as `preset_names` by `app_types()`). "Integrate new app" is a placeholder (to be implemented). The **chatbot** connect form is deliberately minimal: the chatbot type and CLI come from the button clicked (hidden fields), then exactly two visible fields — a workspace folder (path box + **Browse…**, the dialog opens only on Browse) and a free-text **Name** that pre-fills from the chosen folder's name and may be edited to anything. The workspace **path is the chatbot's identity**: a second chatbot for the same path (same type) is refused. The name is only the display label (any text, duplicates allowed); the instance id (its folder under `registered_apps/<type>/`) is the path's own last folder name (`instanceIdForPath` in `app.js`; `-2`, `-3`… if two workspaces share a folder name) and is never shown to the user. Don't reintroduce a separate "Instance ID"/"Display Label" pair or auto-opening dialogs for chatbots; the Obsidian/Claudia (My Apps) forms still use ID + label. Open buttons (home cards, app/chatbot rows) call `/api/apps/open` with the instance's `category` and `dir` folder names; `can_open` is per instance, from the instance's own `init.py` having `launch()`.

Quota/limits and model lists come from the **extractor subsystem** below. Only a **proxy** runs an extractor (for its own provider, lazily via its endpoints); the **router polls each running proxy's `/usage` and `/models` endpoints** at startup and every `--refresh-interval` seconds (default 1800; `0` = startup only) and never reads the status JSON or launches bulk extractor scripts directly.

## Extractor subsystem (`src/tokenbuffet/extractors/`)

Scrapes a vendor CLI's interactive TUI for its `/usage` and `/model` screens, since these aren't available over any API. Two primitives, deliberately split:

- **`capture`** (expensive, live) — `tui.py` drives the real CLI through a pseudo-console (ConPTY via `pywinpty` on Windows, pty via `pexpect` on POSIX — chosen lazily in `_spawn_proc`), feeds the raw escape stream through `pyte` to reconstruct the 2D screen, answers onboarding `gates`, cycles tabbed `views`, and writes cleaned screen text to `data/providers_status/raw/<name>_<op>_raw.txt`.
- **`parse`** (cheap, re-runnable) — `usage.py` / `models.py` run the config's regexes over that saved text to produce structured JSON. Iterate on regexes by re-running `parse` against the saved `_raw.txt`; never re-capture to tune a regex.

Canonical models shape: `models.available` is a list of `{id, name}` objects where **`id` is the exact `--model` CLI argument** (`name` is the friendly TUI label); an optional `id_case` (`"lower"`/`"upper"`) in the models config normalizes the executable `id` while preserving the display `name`. `data/providers_status/<provider>_models.json` is the proxy-owned cache; the proxy's `/models` and `/v1/models` read or refresh it, and the router's one-time populate resolves each tier regex against `/models` to freeze exact ids into `config/router_config.json`.

Canonical usage shape: each `periods` entry yields `{used_pct, remaining_pct, resets}`. `remaining_pct` is canonical — `config.calculation` maps the CLI's printed percentage to it (`100 - float(value)` when the CLI prints percent *used*, `float(value)` when it prints percent *left*) and `used_pct` is derived as the complement. A declared period whose regex doesn't match reports `null`.

`process_env.py` builds the subprocess environment purely from a provider config's `process_env` block (`unset` keys, `set` values with `{repo}` expansion, `mkdir` dirs) — no per-provider special-casing; every provider (agy included) inherits the real user profile unless its config says otherwise.

## App registration (`integrations/` → `registered_apps/`)

Downstream apps are configured by a **three-layer cascade** with the same file set at each layer: base `integrations/` → app-type `integrations/<app>/` (e.g. `obsidian`, `chatbot`) → instance `registered_apps/<app>/<name>/`. `configure`/`init` scripts read sibling JSONs from cwd. An app type's `init.py` may define `check()` (raise if the app isn't installed; run by `add-app`, `doctor`, and the dashboard to hide uninstalled types) `link(app_path)` (make the app itself aware of the instance, e.g. add a vault to Obsidian's vault list; run by `tbuffet demo init`) and `launch(app_path)` (used by `tbuffet open` and the dashboard Open button; both load it from the **instance's own** `registered_apps/<type>/<name>/init.py`, not the type's). `integrations/register.py` applies an instance's `app_config.json` to write the app's `app_settings.json`. The `chatbot` app-type registers CLI agents (Claude-Code, Codex-CLI, Grok-Build, Gemini-Antigravity) as router clients; `demo/chatbots/` holds config examples (not yet run end-to-end).

Chatbot clients use folder presets under `integrations/chatbot/presets/<cli>/`: `app_config.json`
declares the router endpoint, model tier, and native settings path; `app_settings.json` declares
the primary settings and additional `files`, including `launch.json`. Add a client with
`tbuffet add-chatbot grok --path C:\mygrok`, then
`tbuffet open chatbot mygrok`. Registration overwrites existing generated files without backups.
The initializer substitutes `{active_endpoint}` and `{single_model_tier}` from the instance config.
The Hub discovers these presets for its CLI selector. New CLI presets need data files, not engine
branches. Launchers keep settings and required home overrides scoped to the chosen workspace/session.

## Commands

```bash
# Packaged entry point (canonical). Run from the workspace root.
tbuffet init          # scaffold, register provider CLIs found on PATH (no login/quota check), check() app types
tbuffet demo init     # copy demos, link vaults, apply settings, trust and initialize Obsidian via its enabled CLI
tbuffet open <type> <name>   # open a registered app via integrations/<type>/init.py launch()
tbuffet start         # launch all proxies + router (8090) + dashboard (8080); Ctrl+C stops this session's process trees
tbuffet start --debug # also capture full proxy request/response traces
tbuffet start --background # explicitly launch in background; use tbuffet stop to shut down
# equivalently: python -m tokenbuffet.cli {init,start}

# Run one layer directly (debugging):
python -m tokenbuffet.cli_proxy_server --provider claude --port 8001 [--ui-stream true]
python -m tokenbuffet.local_router --port 8090
python -m tokenbuffet.dashboard
```

Extractor capture/parse — use the OS wrapper scripts (they set `PYTHONPATH` and write raw captures to `data/providers_status/raw/`):

```powershell
.\scripts\providers\read-provider.ps1 usage grok           # capture + parse a provider's usage
.\scripts\providers\read-provider.ps1 models grok
.\scripts\providers\read-provider.ps1 usage grok -RawOnly  # capture only
.\scripts\providers\read-provider.ps1 usage grok -Extract data\providers_status\raw\grok_usage_raw.txt   # re-parse saved raw
```
`scripts/providers/read-provider.sh` is the bash equivalent. Under the hood: `python -m tokenbuffet.extractors {capture,parse} <op> <config> ...`.

There is **no test runner, linter, or build step** and there are no unit tests; every package the code uses (`pyte`, `pywinpty`/`pexpect`, `openai`, `ai`) is a plain required dependency in `pyproject.toml` — no optional extras, no "if not installed" fallbacks; captured TUI raw text lands in `data/providers_status/raw/` (gitignored). Validate changes by capturing/parsing a provider and checking the JSON (periods sum to 100, models have no phantom entries).

## Adding / fixing a provider

Use the **`register-provider` skill** (`.claude/skills/register-provider/`) — it is the authoritative how-to (probing the TUI with `scripts/probe_tui.py`, writing the config, the Windows/TUI gotchas). Start a new config from `integrations/providers/template_config.json`; `grok` is the simplest worked example, `agy` the most complex. When you touch the engine, re-parse every existing provider's saved raw and confirm identical output — engine changes must stay generic, config-gated, and default to prior behavior.

## Gotchas

- **Extractor package lives at `src/tokenbuffet/extractors/`** (top-level, not under `tokenbuffet`); invoke as `python -m tokenbuffet.extractors`. The bridge package is `src/tokenbuffet/`.
- **Config paths have no `config/` prefix for providers:** built-in provider configs are `integrations/providers/<name>/config.json` (the catalog), registered ones are copied to `registered_providers/<name>/config.json` (what the engine runs); only the router's `config/router_config.json` lives under `config/`.
- **Usage/models are proxy-owned, not file-scraped by the router.** The old `scripts/providers/read-providers` router-refresh path is gone — the router polls proxy `/usage` + `/models` HTTP endpoints. Don't reintroduce inline scraping or a router-side status-file reader.
- **All dependencies are required** (`pyte`, `pywinpty`/`pexpect`, `openai`, `ai`; Python 3.12+). The `ai.ui.ai_sdk` UI-message stream is still an opt-in *output format* (`--ui-stream true`); there is no `--ollama-fake`.
- **Windows/TUI capture:** on Git Bash prefix probes with `MSYS_NO_PATHCONV=1` (else a `/usage` arg is rewritten to a path) and always `PYTHONIOENCODING=utf-8` (cp1252 console). `clean_screen` turns box/block glyphs — including progress bars `█░` — into spaces and collapses *consecutive* duplicate lines, so parse the numeric `%`, not the bar.
- **`data/`, `logs/`, and sandbox temp dirs are gitignored** — runtime logs, scraped status, provider homes. `registered_providers/<name>/config.json` and the `default_templates/` copies are the tracked source of truth.
- **`graphify/` is a separate sub-project** (graph-only Obsidian second-brain design), distinct from the bridge runtime; design docs are under `docs/` (infrastructure, integrations, dashboard, planning subfolders).

Obsidian demo setup is file-only and needs no running Obsidian: `tbuffet demo init` copies the vaults (the plugin, its `data.json` with `llmReady: true`, and the `wiki/` folders ship in the demo), applies settings and adds each vault to Obsidian's `obsidian.json` vault list via `link()`. The plugin falls back to `data.json`'s `apiKey` (`TokenBuffet`) when its SecretStorage entry is empty (`resolveProviderApiKey` in the bundled plugin), so no secret is written. Obsidian keeps its vault trust in the app's own `localStorage` (`enable-plugin-<vault id>`, inspected in Obsidian 1.14.4), which setup cannot write, so the first open of each vault shows Obsidian's **Trust author and enable plugins** dialog. The enabled Obsidian CLI (https://obsidian.md/help/cli) is needed only by `tbuffet open`.

The Claudia demo's `prepare_demo(app_path)` hook runs Claudia's own installer (`npx get-claudia claude . --yes`, per its README) in the demo workspace, which sets up the memory daemon and `.mcp.json`, then re-applies the router endpoint to `.claude/settings.local.json`. It needs Node.js (`npx`) on PATH.
