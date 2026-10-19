---
name: register-provider
description: This skill should be used when the user asks to "register a provider", "add a provider", "add <CLI> to LLMCLIExtractors", "continue with <CLI>", or to extract models/usage/quota from a new LLM CLI's interactive TUI (e.g. codex, grok, Codex, agy/antigravity, gemini). Guides probing a CLI's TUI, writing its registered_providers/<name>/config.json, and validating capture + parse.
version: 0.1.0
---

# Register a provider (LLM CLI TUI extractor)

## Purpose

This repo is a config-driven harness that drives a third-party LLM CLI's
interactive TUI and scrapes its `/model` and `/usage` screens. Adding a provider
means adding a declarative `registered_providers/<name>/config.json` — generic
Python reads it; there are no provider-specific code branches. This skill
captures the end-to-end procedure for registering one, plus the Windows/TUI
gotchas that are non-obvious and cost time every single time.

## When to use

Use when registering, adding, or debugging a provider for this repo — a new CLI,
or fixing an existing provider whose capture/parse is wrong. Read
`AGENTS.md` first for architecture; this skill is the how-to.

## Workflow (five steps)

1. **Fingerprint the CLI.** `which <cmd>`, `<cmd> --version`, `<cmd> --help`.
   Note the launch argv and any inline/non-fullscreen flag
   (`grok --no-alt-screen`, `codex --no-alt-screen --no-daemon`). That argv
   becomes `cli_cmd`. Usage is always scraped from the live TUI; the `models` op
   may instead run a non-interactive subcommand (`list_cmd`) when the TUI picker
   shows only friendly names and the CLI can print real `--model` IDs.

2. **Probe the TUI — SEE the screens before writing config.** Use the bundled
   `scripts/probe_tui.py` to print the boot screen, slash menu, and panels.
   Do not guess gate text, command names, or timing. On Git Bash, prefix with
   `MSYS_NO_PATHCONV=1` (else a `/usage` arg is rewritten to a path) and always
   `PYTHONIOENCODING=utf-8`:

   ```
   MSYS_NO_PATHCONV=1 PYTHONIOENCODING=utf-8 PYTHONPATH=. \
     python .Codex/skills/register-provider/scripts/probe_tui.py \
       --cli <cmd> --gate-when "do you trust" --command /usage --submit-wait 1.5 --view-wait 6
   ```

   Use `--explore` (types `/`) to list slash commands; `--boot-wait N` for boot;
   `--tabs N` to cycle tabbed views. See `references/workflow.md` for the probe
   recipes and how to read each screen.

3. **Write `registered_providers/<name>/config.json`.** Start from
   `integrations/providers/template_config.json` (authoritative schema) or copy a
   sibling — `grok` is the simplest, `agy` the most complex (gated boot,
   autocomplete `submit_wait`, grouped limits, header/footer scan bounds). Key
   decisions, detailed in `references/workflow.md`:
   - `gates` for onboarding prompts (`[{when, send, wait}]`, fires only if shown).
   - `submit_wait` (e.g. 1.5) if the CLI shows a slash-command autocomplete popup
     (codex, agy); without it the command sits unsubmitted in the input box.
   - usage `periods` = one `{pct, resets}` per concurrent limit; grouped/multiple
     limits flatten into separate period names with group-anchored regexes.
   - `calculation` maps the captured percentage to canonical `remaining_pct`
     (`used_pct` is derived as its complement): `100 - float(...)` when the CLI
     prints percent USED, `float(...)` when it prints percent LEFT.
   - models: prefer `list_cmd` (a models subcommand, e.g. `["grok","models"]`) so
     the list carries the real `--model` IDs, not just the TUI's friendly names;
     else drive the TUI picker with `list_start`/`list_end` bounding the scan.
     `list_regex` feeds `parse_models`, which emits `{id, name}` per model — name
     the `(?P<id>)`/`(?P<name>)` groups to split them, one group means id == name.

4. **Capture, then iterate parse for free.** Capture is expensive (live TUI);
   parse is cheap and re-runnable over the saved `_raw.txt`:

   ```
   PYTHONIOENCODING=utf-8 PYTHONPATH=. python -m tokenbuffet.extractors capture <op> registered_providers/<name>/config.json tests/<name>_<op>_raw.txt
   PYTHONIOENCODING=utf-8 PYTHONPATH=. python -m tokenbuffet.extractors parse   <op> registered_providers/<name>/config.json tests/<name>_<op>_raw.txt tests/<name>_<op>.json --provider <name>
   ```

   `<op>` is `models` or `usage`. Read the actual `_raw.txt` to confirm what
   `clean_screen` produced, then tune regexes and re-run `parse` only. The OS
   scripts `scripts/read-provider.ps1` / `scripts/read-provider.sh` wrap this
   (`-Extract` / `--extract` = re-parse a saved raw).

5. **Validate.** config is valid JSON; models `available`/`default` correct with
   no phantom entries; every usage period has `used_pct`+`remaining_pct` summing
   to 100 and a `resets`; `plan` populated. If the engine was touched, re-parse
   every existing provider's saved raw and confirm identical output — engine
   changes must be generic, config-gated, and default to prior behavior.

## Critical gotchas (all learned the hard way)

- **Git Bash mangles leading slashes** → `MSYS_NO_PATHCONV=1` on probes (shipped
  `command` in JSON is immune). **cp1252 console** → `PYTHONIOENCODING=utf-8`.
- **Autocomplete popup** eats a combined command+Enter → `submit_wait`.
- **`clean_screen` turns box/block glyphs (incl. progress bars `█░`) into
  spaces** and drops only CONSECUTIVE duplicate lines — parse the numeric `%`,
  not the bar; non-adjacent repeated labels survive for group anchoring.
- **CLIs report used OR remaining** — normalize with `calculation`, never assume.
- **Header/footer echo the current model** → bound the model scan.
- **TUI model picker shows friendly names, not `--model` IDs** → use a `list_cmd`
  subcommand for the real IDs; `parse_models` returns `{id, name}` per model.

## Additional resources

- **`references/workflow.md`** — full step-by-step with every gotcha, regex
  examples, `clean_screen` transforms, and the "when the engine needs a knob"
  rule (precedents: `submit_wait`, `list_start`/`list_end`, used/remaining).
- **`scripts/probe_tui.py`** — parameterized ConPTY+pyte TUI probe for discovery.
- Repo files to lean on: `AGENTS.md` (architecture), `integrations/providers/template_config.json`
  (schema), and the `grok`/`codex`/`agy` configs as graded examples.
