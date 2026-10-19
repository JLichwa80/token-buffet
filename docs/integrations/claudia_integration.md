# Claudia Integration

Status: scaffold complete (`integrations/claudia/`); direct routing implemented. Demo instance in `registered_apps/claudia/`.

## What Claudia is

Claudia ([github.com/kbanc85/claudia](https://github.com/kbanc85/claudia)) is a local
**Claude Code–based "second brain"**: a persona + ~45 skills, a Python **memory daemon** (MCP,
~33 tools over SQLite + vector embeddings), and an Obsidian **vault projection** at
`~/.claudia/vault/` (wiki-style synthesized topic pages with `[[wikilinks]]`, PARA layout) whose
graph is rendered by the **`/brain` 3D brain-graph visualizer** ("graphify"). Stock upstream
runs **only on Claude Code and has no model routing**. The Token Buffet integration adds routing
so every Claude Code call routes across all subscriptions.

## Wiring

Claude Code is pointed at the router via `ANTHROPIC_BASE_URL` in `.claude/settings.local.json`.
The router speaks the Anthropic Messages wire on `/v1/messages`, so no LiteLLM hop is needed.

```
Claudia (Claude Code) → router :8090 → proxy → vendor CLI
```

Tier map: `opus → reasoning`, `sonnet → medium`, `haiku → fast`.

## Registration

`integrations/claudia/` app type:
- `app_config.json` — `path` is the Claudia workspace root; `client_settings` supplies the endpoint and model tier.
- `app_settings.json` — sets `ANTHROPIC_BASE_URL: http://127.0.0.1:8090/client/claude` and `ANTHROPIC_AUTH_TOKEN: local-bridge` in `.claude/settings.local.json`.
- `init.py` — writes/merges the redirect into the Claude folder's `settings.local.json`.
- Its `launch(app_path)` hook enables the Hub's existing **Open** button. On Windows it opens
  a visible PowerShell terminal running `claude` in the registered workspace. It requires Claude Code
  on PATH and an existing workspace containing `CLAUDE.md`.

Register an instance:
```
tbuffet add-app claudia "My Claudia" --path "/path/to/claudia"
```

The demo instance is registered at `registered_apps/claudia/My-Client-Relationships-Management/`.

## The bigger story

Both Claudia's vault and the LLM-wiki are karpathy-style wikis. The "second brain + wiki" demo is
Claudia's `/brain` graph over a vault that Token Buffet powers end to end: Claude Code (Claudia) →
bridge → subscription CLIs, while memory and vault stay local.

## Open items

- Does the `agy` (Gemini Antigravity) backend support Claudia's MCP tool protocol? (unverified)
- PDF/image ingestion from within Claudia sessions — blocked until multimodal proxy forwarding lands (see [futureideas.md](../planning/futureideas.md)).
