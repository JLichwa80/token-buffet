# Registering a provider — full workflow and gotchas

Detailed companion to SKILL.md. Read this when actually registering a provider.
Everything here was learned registering grok, claude, codex, and agy.

## The two-phase pipeline this plugs into

- **capture** (expensive): drives the live TUI, cleans the screen, writes
  `tests/<provider>_<op>_raw.txt`.
- **parse** (cheap, re-runnable): runs regexes over a saved `_raw.txt`, writes
  `tests/<provider>_<op>.json`.

Capture once, then iterate regexes for free against the saved raw. Entry points:

```
python -m tokenbuffet.extractors capture <op> <config> <out_raw.txt>       # op = models | usage
python -m tokenbuffet.extractors parse   <op> <config> <raw.txt> <out.json> --provider <name>
```

Always set `PYTHONPATH` to the repo root. On Windows always set
`PYTHONIOENCODING=utf-8` (box/braille glyphs crash the default cp1252 console).
The OS scripts (`scripts/providers/read_provider_status.ps1` / `scripts/providers/read_provider_status.sh`) wrap these and own
naming; the re-parse path is `-Extract <raw>` (ps1) / `--extract <raw>` (sh).

## Step 1 — Locate and fingerprint the CLI

```
which <cmd>            # or: where on PowerShell
<cmd> --version
<cmd> --help | head -80
```

Look for an **inline/non-fullscreen flag** (`grok --no-alt-screen`,
`codex --no-alt-screen --no-daemon`). agy had none and still worked — pyte
reconstructs the alternate screen anyway — but prefer the flag when offered: it
keeps scrollback and avoids alt-screen quirks. Note the exact launch argv; it
becomes `cli_cmd`.

A CLI may also expose non-interactive subcommands (`grok models`, `agy models`).
Usage/quota is always scraped from the live TUI. Models is the one exception: the
TUI `/model` picker shows only FRIENDLY names, so when a models subcommand prints
the real `--model` IDs, set `list_cmd` and capture shells out for that op (Step 3).
Note the subcommand's argv.

## Step 2 — Probe the TUI with scripts/probe_tui.py

Do NOT guess at config values. SEE the screens first. The probe prints the raw
pyte grid after boot, after the gate, and after a command.

```
# boot screen (+ any trust/onboarding gate)
MSYS_NO_PATHCONV=1 PYTHONIOENCODING=utf-8 PYTHONPATH=. \
  python .claude/skills/register-provider/scripts/probe_tui.py --cli <cmd> --boot-wait 10

# slash-command menu — find the model/usage command names
... probe_tui.py --cli <cmd> --gate-when "<gate text>" --explore

# open a panel; bump --submit-wait / --view-wait until it renders
... probe_tui.py --cli <cmd> --gate-when "<gate text>" --command /usage --submit-wait 1.5 --view-wait 6
```

Filtering the slash menu: `--explore` only types `/`. To filter further, run
the probe with `--command /mod` style and read the autocomplete list (it shows
matching commands with descriptions).

### Windows shell gotchas (both real, both bite immediately)

- **Git Bash mangles leading slashes.** `/usage` becomes `C:/Program Files/Git/usage`
  before Python sees it. Fix: prefix with `MSYS_NO_PATHCONV=1`, or run from
  PowerShell. (The shipped `command` in config.json is immune — it lives in JSON,
  read by Python, never touched by the shell.)
- **cp1252 console.** Always `PYTHONIOENCODING=utf-8` when printing captured text.

## Step 3 — Model the screens into config.json

Create `registered_providers/<name>/config.json` with `models` and/or `usage`
sections. `integrations/providers/template_config.json` is the authoritative
schema; copy a sibling (`grok` simplest, `agy` most complex) as a starting point.

### Trust / onboarding prompts — three ways, pick per provider

First-run prompts like "Do you trust the contents of this project?" steal focus
and block the command. Options, in order of preference:

1. **Pre-grant via a repo-local settings file** (best when the CLI reads cwd/
   project-local config): drop the CLI's native trust/permission file at the
   repo root so the prompt never appears — e.g. `.grok/trusted_folders.toml`
   (`[folders.'<abs path>']` `trusted = true`), `.codex/config.toml`
   (`sandbox_mode = "danger-full-access"`, `approval_policy = "never"`). Verify
   it is honored (grok: `grok inspect` shows "Project trusted: yes").

2. **`expect` readiness gate + manual trust** (when the CLI only keeps trust in
   its GLOBAL config, e.g. agy/antigravity, so a repo-local file is inert):
   declare an `expect` marker that only appears once the real panel loads
   (agy models `"Switch Model"`, usage `"Models & Quota"`). If capture cannot
   reach it, the pipeline errors out and tells the user to run the CLI here once
   and trust the folder. Do NOT auto-answer the trust prompt in this case — the
   point is to surface the untrusted state, not silently accept it.

3. **`gates`** — auto-answer the prompt when that is acceptable:

   ```json
   "gates": [{"when": "do you trust", "send": "\r", "wait": 4}]
   ```

   `when` is matched case-insensitively; the gate fires only if present, so it
   is safe whether or not the prompt appears. The send is the ANSWER for that
   CLI's widget: agy's is a highlighted menu → `"\r"` (Enter), not `"y\n"`.

**Bypass flags do not cover folder trust.** `agy --dangerously-skip-permissions`
(and claude's equivalent) only auto-approve *tool permission* requests, which a
read-only `/usage`/`/model` capture never triggers — verified that agy still
shows its trust gate with the flag set. Add such a flag to `cli_cmd` only to
future-proof tool prompts; it will not replace options 1–3 for trust.

**A bypass flag can introduce its OWN prompt.** claude's
`--dangerously-skip-permissions` triggers a "Bypass Permissions mode" acceptance
screen that blocks the TUI until answered. Gate it
(`{"when": "Bypass Permissions", "send": "y\r", "wait": 4}`) AHEAD of the trust
gate — the gate loop re-snapshots per gate, so order them boot-prompt-first.
Symptom of a missing gate here: capture exits 0 but every period parses `null`
because `/usage` never ran.

### submit_wait — autocomplete-popup TUIs

Some TUIs (codex, agy) show a slash-command AUTOCOMPLETE popup; a combined
`command + Enter` write gets swallowed and the panel never opens. Set
`submit_wait` (e.g. `1.5`) so the driver types the command, pauses, then sends
Enter separately. grok/claude submit fine with `submit_wait` absent (0 =
legacy combined write). Symptom of a missing submit_wait: the command text is
left sitting in the input box in the capture.

### Timing knobs

`boot_wait` (until the welcome screen settles), `view_wait` (after the command /
each Tab). agy needed `boot_wait: 10`, `view_wait: 4`. Panels that "Generating..."
need a larger `view_wait`. `cols` (200) / `rows` (50) size the grid — raise
`rows` if a tall panel is cut off.

### models section

The TUI `/model` picker shows FRIENDLY names, not the string the CLI accepts as
`--model`. Prefer a non-interactive subcommand when the CLI has one; fall back to
the TUI picker when it does not.

**Preferred — non-interactive `list_cmd`.** Set the argv of a models subcommand
and capture shells out for the `models` op instead of driving the TUI:

```json
"list_cmd": ["grok", "models"],   // run non-interactively; its stdout is parsed
"list_timeout": 60,                // optional, seconds (default 60)
"list_regex": "^[*-]\\s+(\\S+)",
"default_marker": "(default)"
```

**Fallback — TUI picker.** Omit `list_cmd`; capture drives `/model` and parses the
snapshot (`cli_cmd`, timing knobs, and `list_start`/`list_end` all apply).

`list_regex` runs per line (`re.search`) over whichever text was captured.
`parse_models` emits one `{id, name}` per match, deduped by id:

- Name the groups to split id from friendly name — agy's
  `^(?P<id>[a-z][\\w.]*-[\\w.\\-]+)\\s+(?P<name>.+)$`.
- A single unnamed group sets `id == name` — grok/codex, whose subcommand prints
  one token per line (`^[*-]\\s+(\\S+)`).
- A line containing `default_marker` tags that entry's id as `default`.

**Header/footer contamination (TUI path only):** many TUIs echo the current model
in a header (`Gemini 3.1 Pro (High)`) and footer (`Gemini 3.1 Pro · high`). Those
lines match a loose `list_regex` and create phantom entries. Bound the scan with
`list_start`/`list_end` (substrings marking the picker region) instead of fighting
it in the regex. Omit both to scan the whole screen.

### usage section

```json
"extractors": { "plan": "REGEX one group" },
"periods": { "<name>": { "pct": "REGEX one group", "resets": "REGEX one group" } },
"calculation": "EXPR -> remaining_pct from captured `value`",
"limit": 100
```

- **`extractors`** — flat descriptive fields (e.g. `plan`). Dotted keys nest via
  `set_path`. Anchor to something stable: agy's plan is in the header
  `email (Google AI Pro)` → `"[\\w.+-]+@[\\w.-]+\\s*\\(([^)]+)\\)"`.
- **`periods`** — one entry per concurrent limit, each a `{pct, resets}` pair.
  `pct` captures whatever percentage the CLI prints.
- **`calculation`** — maps the captured `value` to the canonical `remaining_pct`;
  `used_pct` is DERIVED as its complement, so the two always sum to 100. This is
  the key normalization: it does not matter whether the CLI reports USED or LEFT.
  - CLI prints percent **USED** (grok 80%, claude "73% used"):
    `"100 - float(str(value).strip('%'))"`
  - CLI prints percent **LEFT/REMAINING** (codex "100% left", agy "17.03%"
    remaining): `"float(str(value).strip('%'))"`
  - Evaluated by `safe_calc` in a locked-down namespace (only `value`, `limit`,
    and a few numeric builtins).

**Grouped / multiple limits** flatten into separate period names. agy shows two
model groups each with a weekly + 5-hour limit → four periods
(`gemini_weekly`, `gemini_5h`, `claude_gpt_weekly`, `claude_gpt_5h`), each regex
anchored on its group header:
`"GEMINI MODELS.*?Weekly Limit Remaining.*?([\\d.]+)%"`. Regexes run with
`DOTALL | IGNORECASE`; use non-greedy `.*?` and anchor on section headers so a
later group's number is not captured for an earlier one.

A declared period whose `pct` regex does not match is reported as `null` (N/A) —
safe for a period that is only sometimes shown (grok's daily).

## Step 4 — How clean_screen shapes the text you regex against

`capture` runs `util.clean_screen` before writing the raw. Regexes see the
CLEANED text, so know its transforms:

- Box-drawing + block glyphs U+2500–U+259F (borders, separators, **progress
  bars** `█░`) → spaces. Do not try to parse the bar; read the numeric `%`.
- Decorative glyphs (braille spinner/logo, geometric bullets `●◆`, `❯`, arrows)
  → spaces.
- Each line: runs of whitespace collapse to one, then trimmed.
- Dropped: blank lines, punctuation-only lines, and **consecutive** duplicate
  lines. Only consecutive — agy's two non-adjacent "Weekly Limit Remaining"
  labels both survive, which is why group-anchored period regexes work.
- `strip_lines` (config) drops whole lines containing any listed substring
  (telemetry/opt-in banners). `strip_terms`/`drop_lines` are the `clean_screen`
  args behind it.

Verify assumptions by reading the actual `tests/<provider>_<op>_raw.txt` after
capturing, not by imagining the screen.

## Step 5 — Capture, iterate, validate

```
# capture both ops (expensive, drives the live TUI)
PYTHONIOENCODING=utf-8 PYTHONPATH=. python -m tokenbuffet.extractors capture models registered_providers/<name>/config.json tests/<name>_models_raw.txt
PYTHONIOENCODING=utf-8 PYTHONPATH=. python -m tokenbuffet.extractors capture usage  registered_providers/<name>/config.json tests/<name>_usage_raw.txt

# iterate regexes against the saved raw for free
PYTHONIOENCODING=utf-8 PYTHONPATH=. python -m tokenbuffet.extractors parse models registered_providers/<name>/config.json tests/<name>_models_raw.txt tests/<name>_models.json --provider <name>
PYTHONIOENCODING=utf-8 PYTHONPATH=. python -m tokenbuffet.extractors parse usage  registered_providers/<name>/config.json tests/<name>_usage_raw.txt  tests/<name>_usage.json  --provider <name>
```

Checklist before declaring done:

1. `config.json` is valid JSON (`python -c "import json;json.load(open(...))"`).
2. models: `available` has every picker entry, no header/footer phantoms,
   `default` is the current model.
3. usage: every period has sane `used_pct`/`remaining_pct` summing to 100, and a
   `resets` string; `plan` is populated.
4. **No regression** — if the engine (`tokenbuffet.extractors/*.py`) was touched to support
   this provider, re-parse every existing provider's saved raw and confirm
   output is unchanged. Engine changes must be config-driven and default to the
   old behavior (no provider-specific branches — see CLAUDE.md).
5. The `_raw.txt` fixtures are committed (they power the `--extract` re-parse
   path); the `.json` outputs are git-ignored.

## When the engine genuinely needs a new knob

Adding a provider should normally be config-only. If a provider needs behavior
the engine lacks, add a GENERIC, config-gated knob that defaults to existing
behavior — never an `if provider == ...` branch. Precedents:

- `submit_wait` in `tui.py` (codex/agy autocomplete) — default 0 = unchanged.
- `used_pct`→complement-of-`remaining_pct` in `usage.py` — made "reports left"
  work without touching grok/claude output.
- `list_start`/`list_end` in `models.py` (agy header/footer) — omitted = scan all.

Update CLAUDE.md, README.md, and template_config.json whenever a knob is added.
