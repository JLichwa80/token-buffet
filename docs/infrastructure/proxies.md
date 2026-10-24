# Provider Proxies

A **proxy** (`src/tokenbuffet/cli_proxy_server.py`) turns one vendor CLI (Claude Code, Codex, Grok Build, Gemini Antigravity) into a local HTTP API. There is one proxy process per provider, bound to `127.0.0.1`. Everything provider-specific lives in `registered_providers/<name>/config.json`; the engine has no per-provider branches.

| Provider | Default port | CLI |
|---|---|---|
| grok | 8000 | `grok` |
| claude | 8001 | `claude` |
| codex | 8002 | `codex` |
| agy | 8003 | `agy` |

If the configured port is taken by another process, the proxy binds the next free one and publishes it to `data/providers_status/<provider>_run_status.json`. Clients (the router) read the port from that file.

A proxy does two independent jobs:

1. **Prompt processing**: answer chat requests by running the CLI once per request.
2. **Usage and model extraction**: read the CLI's quota and model list by driving its interactive screens, and cache them.

The proxy never calls a vendor API itself. The CLI does, with the user's own login. The proxy only translates between HTTP and the CLI.

---

## 1. Prompt processing

### Wire formats

Every proxy serves **every** wire format; the format is chosen by the request path, not by the provider.

| Path | Format |
|---|---|
| `/v1/chat/completions`, `/api/chat` | OpenAI chat / Ollama chat |
| `/v1/completions`, `/api/generate` | OpenAI text / Ollama generate |
| `/v1/responses`, `/v1/chat/responses` | OpenAI Responses (events built through the `openai` SDK's Pydantic types) |
| `/v1/messages` | Anthropic Messages (text and tools) |
| `/v1/models/{model}:generateContent`, `:streamGenerateContent` (also `/v1beta/...`) | Gemini GenerateContent |

`--ui-stream true` switches the OpenAI/Ollama paths to the Vercel `ai_sdk` UI-message stream (opt-in output format).

The `server.protocol` value in each config (currently `responses` for all four) is only the proxy's default label; it does not restrict which paths work.

### Request pipeline

1. **Parse** the body for the path's format. Gemini and Anthropic bodies are validated and normalized first; Responses `input` is turned into messages.
2. **Flatten to one prompt.** Messages become `[ROLE]:\ncontent` blocks joined by blank lines. Anthropic `system` and Responses `instructions` become a leading `[SYSTEM]:` block. List-style content keeps only its text parts.
3. **Tool handoff** (only when the request carries client tools, or a tool history). `tool_wire.py` prepends an instruction asking the model for one structured tool-call decision, and the history of earlier calls and results is rendered into the prompt. The proxy returns that decision to the client in the client's own format; **the client executes the tool**, not the bridge. The provider config may add `execution.tool_handoff_args` (claude and grok use `--tools ""`) so the CLI does not run its own tools for these requests.
4. **Build the command** from `execution`:
   - `cmd_template`: `{prompt_file}` is replaced by a temp file holding the prompt, `{prompt}` by the prompt inline.
   - `model_arg`: appends the requested `model` verbatim (e.g. `--model {model}`). The id must be one the CLI accepts; see section 2.
   - `effort_arg`: appends `effort` / `reasoning_effort` from the request, when present.
   - `tool_handoff_args`: appended in tool mode.
5. **Build the environment** from the config:
   - `env_unset`: keys removed so the CLI uses its own login instead of an inherited API key or base URL (claude: `ANTHROPIC_*`; codex: `OPENAI_*`; agy: `GOOGLE_GEMINI_BASE_URL`, `GEMINI_API_KEY`).
   - `isolated_home`: runs the CLI with `HOME`/`USERPROFILE` pointed at a private folder (agy: `data/provider_homes/agy`, with a settings file that denies the CLI's own tools).
   - `sandbox`: when enabled (grok), each request runs against a fresh temp dir holding a copy of the auth file, selected through the config's `env_var` (`GROK_HOME`), and deleted afterwards.
6. **Spawn the CLI** as a normal subprocess with piped stdin/stdout/stderr (no pseudo-console on this path). The prompt is delivered by `execution.input_method`: `file` (via `{prompt_file}`), `stdin` (written then closed), or `stream-json` (one JSON user event on stdin).
7. **Parse stdout** line by line as JSON and apply `stream` rules from the config:
   - `text_extractors`: each has `matches` (key/value conditions on the JSON line, dotted paths allowed) and `path` (where the text is; `[]` joins over a list). Matching text is appended.
   - `error_extractors`: same shape; a match records a provider error.
   - `done_when`: optional terminal event; once seen, the proxy stops waiting and kills a CLI that has not exited.
8. **Respond in the request's format.**
   - `stream: true`: each extracted piece is written to the client as it arrives (SSE, or NDJSON for Ollama). Anthropic streams send a `ping` every 10 s.
   - Not streaming: the text is collected in memory and returned as one JSON object.
   - Tool mode: the whole CLI output is buffered, parsed into a decision, then sent as tool calls or text. Streaming clients get heartbeat chunks while it waits.
9. **Fail fast.** A non-zero exit, a provider error, or an empty answer is returned as an error (HTTP 502, or an error event if the stream already started). Nothing is retried or substituted. The CLI process is always killed and the temp files removed at the end.

Token counts are not available: `usage` fields are zero placeholders (Anthropic responses carry the header `X-CLI-Bridge-Usage: unavailable; zero counts are placeholders`).

### Logging

Console lines per request: `REQUEST`, `SPAWN`, `FIRST_OUTPUT`, `TEXT`, `WAIT` (no output for 30 s, repeated), `EXIT`, `DONE` or `FAIL`. A per-request session log is written under `logs/<provider>/proxy/sessions/`. With `tbuffet start --debug`, raw requests, CLI stdout/stderr and HTTP bodies are saved too.

---

## 2. Usage and model extraction

Quota and model lists are not available from any API, so the proxy reads them from the CLI's own screens. This is the extractor subsystem (`src/tokenbuffet/extractors/`), which has two deliberately separate steps:

- **capture** (slow, live): gets the screen text.
- **parse** (cheap, re-runnable): runs the config's regexes over the saved text.

To tune a regex, re-run parse on the saved capture in `data/providers_status/raw/<provider>_<op>_raw.txt`; do not re-capture.

### Capture

Two sources, chosen per `usage` / `models` block in the config:

- **`type: tui`**: `tui.py` starts the real CLI in a pseudo-console (ConPTY via `pywinpty` on Windows, a pty via `pexpect` on macOS/Linux), then:
  1. waits `boot_wait`;
  2. answers onboarding **`gates`** (`when` text seen on screen → `send` keys);
  3. types `command` (e.g. `/usage`, `/model`, `/status`);
  4. snapshots the screen, and for multi-tab screens sends `tab_switch` and snapshots again, `views` times.

  The screen is reconstructed with `pyte` (a terminal emulator) because a TUI paints with cursor moves, so the raw stream has no usable line layout. `clean_screen` then turns box and bar glyphs into spaces, drops `strip_lines`, and collapses repeated lines.
- **`list_cmd`** (models only): runs a plain subcommand such as `grok models` or `agy models` with stdin closed. This is preferred where it exists because it prints the exact `--model` id, which the TUI picker does not (it shows friendly labels).

An optional `expect` marker guards the capture: if the marker is missing, the CLI never reached the real screen (not signed in, onboarding or trust unfinished) and the capture fails with the partial screen saved for inspection.

The capture process runs with the provider's `process_env` applied.

### Parse: usage

Per `usage` block:

- `periods`: a map of period name → `pct` (regex whose group 1 is the percentage the CLI prints), `resets` (regex), and optionally `exhausted` (a message that means the limit is hit, which forces `remaining_pct: 0`).
- `calculation`: turns the printed percentage into **`remaining_pct`**: `100 - float(value)` when the CLI prints percent used, `float(value)` when it prints percent left. `used_pct` is the complement, so the two always sum to 100.
- `extractors`: flat descriptive fields, e.g. `plan`.
- A declared period whose regex does not match is reported as `null`. If no period yields a percentage, parsing fails and the proxy reports usage as unavailable.

Result, in `data/providers_status/<provider>_usage.json`:

```json
{
  "provider": "claude",
  "usage": {
    "plan": "Claude Pro",
    "limits": {
      "session": {"used_pct": 0.0,  "remaining_pct": 100.0, "resets": "5:49pm"},
      "weekly":  {"used_pct": 34.0, "remaining_pct": 66.0,  "resets": "Oct 27, 10:59am"}
    },
    "gathered_at": "2026-10-23T13:54:43-07:00"
  }
}
```

Providers differ in which periods they expose (claude: session and weekly; grok: weekly), but all are described the same way in config.

### Parse: models

`list_regex` is applied to each line (optionally bounded by `list_start` / `list_end`). Named groups `id` and `name` fill the entry; with a single group it serves as both. `default_marker` (e.g. `(selected)`, `(default)`, `(current)`) marks the default. `id_case` (`lower` / `upper`) normalizes the executable id while keeping the display name. Duplicates are dropped.

**`id` is exactly what is passed to `--model`**; `name` is the friendly label.

```json
{
  "provider": "claude",
  "models": {
    "available": [
      {"id": "Opus",   "name": "Opus 5.5"},
      {"id": "Sonnet", "name": "Sonnet 5.5"},
      {"id": "Haiku",  "name": "Haiku 5.5"}
    ],
    "default": "Sonnet"
  }
}
```

### Capabilities

A model's capabilities are **not** extracted. The model entry contains only `id`, `name` and the `default` flag; nothing records vision, context window, tool support or thinking. What the bridge does know about capabilities is declared, per provider, in config:

| Config key | Meaning |
|---|---|
| `tiers` | Case-insensitive regexes mapping `fast` / `medium` / `reasoning` to model ids. The router resolves them once, against the `/models` list, to the newest matching id and freezes the result in `config/router_config.json`. |
| `execution.effort_arg` | Whether and how the CLI takes a reasoning effort. |
| `execution.tool_handoff_args` | How to stop the CLI running its own tools when a client supplies tools. |
| `tools` | The CLI's own tools (`available` / `enabled`) and how they are passed. |

Extracting real per-model capabilities would need a source for them (a CLI subcommand or a screen that prints them) and a new field in the models config; neither exists today.

### Refresh and serving

- At startup the proxy binds its port first, then reads usage and models **in a background thread**, so it is usable immediately. On failure it retries every 300 s; on success it refreshes every `--refresh-interval` seconds (default 1800; `0` = once).
- `GET /usage`, `/models`, `/v1/models`, `/api/tags`:
  - If the saved export is younger than the refresh interval, it is returned from disk.
  - If it is stale, the endpoint runs a capture and parse first (up to 180 s per step), so a stale request is not instant.
  - If a capture is already running, the last saved export is returned instead of queueing, or **503** `still being read` when none exists.
  - If a refresh fails, the previous export is kept and returned rather than overwritten.
- `/v1/models` and `/api/tags` are the same model list in OpenAI and Ollama shape (`/api/tags` fills placeholder size and family fields).
- Files in `data/providers_status/`:
  - `<provider>_usage.json`, `<provider>_models.json`: the exports above.
  - `<provider>_run_status.json`: `status` (`starting`, `running`, `stopped`, `failed`), `port`, `pid`, and `usage: {state: reading | ready | unavailable, reason}`.
  - `raw/`: the cleaned captures.

The router polls each running proxy's `/usage` and `/models` over HTTP; it never reads these files or runs the extractors itself. See `router.md`.

### Adding or fixing a provider

Use the `register-provider` skill. Start from `integrations/providers/template_config.json`; `grok` is the simplest example and `agy` the most complex.
