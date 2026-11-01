# Architecture and flow

## End-to-end flow

```
Obsidian vault
  _Inbox/*.md  (watched folder)
        |
        v
Karpathy LLM Wiki plugin  (.obsidian/plugins/karpathywiki/)
  provider: custom-responses
  baseUrl:  http://127.0.0.1:8090/v1/
  model:    a router tier (fast | medium | reasoning), per task
        |  POST /v1/responses
        v
Token Buffet router :8090          config/router_config.json
  tier -> {provider, model, effort}; mode usage (most quota left) or custom (custom_order)
        |
        v
Provider proxy (one per CLI)       registered_providers/<name>/config.json
  flattens the request to a text prompt, spawns the vendor CLI, parses its stream
        |
        v
Claude / Codex / Grok / agy CLI    (your flat-rate subscription)
        |
        v  streamed text back up the same chain
        |
Plugin writes wiki/sources, wiki/entities, wiki/concepts, index.md, log.md
```

Three long-running processes are involved (see the architecture section of the main `CLAUDE.md`): the provider **proxies**, the **router**, and the **dashboard** (8080: router, quota and request activity). The plugin never talks to a CLI directly.

## What each layer owns

| Layer | Owns | Does not own |
|---|---|---|
| Plugin | Prompts, page templates, tag vocabulary, retrieval and graph logic, the wiki files | Which model or subscription answers |
| Router | Tier to model/provider choice, quota balancing, effort injection | Anything about wiki content |
| Proxy | Spawning the CLI, wire formats, stream parsing | Routing decisions |
| Obsidian integration (`integrations/obsidian/`) | Writing the plugin's settings, vault registration and launch | Running the plugin |

The engine has no Obsidian-specific code. Everything Obsidian-specific is data and small hooks under `integrations/obsidian/` ([implementation.md](implementation.md)).

## Data on disk

```
<vault>/
  _Inbox/                          raw sources (never modified)
  wiki/
    sources/ entities/ concepts/   generated pages
    schema/config.md               vocabulary and templates
    index.md  log.md               generated directory and operation log
  .obsidian/plugins/karpathywiki/
    data.json                      settings (written by Token Buffet)
    main.js manifest.json styles.css
registered_apps/obsidian/<name>/   Token Buffet registration for the vault
```

## Request path per task

| Plugin task | Tier | Why |
|---|---|---|
| Ingest (extraction, page generation, merge) | `fast` | Many small calls per note |
| Lint, Smart Fix All | `reasoning` | Judgment on duplicates and contradictions |
| Query | `reasoning` | Synthesis with citations |

The router resolves the tier to a concrete CLI model and adds an effort level (`fast`=low, `medium`=medium, `reasoning`=high unless overridden). See [router.md](../../infrastructure/router.md).

## Failure behavior

- Router or proxies not running: plugin calls fail with a connection error and nothing is written for that note.
- Quota exhausted on a backend: in `usage` mode the router skips depleted backends; the quota cache is only as fresh as `--refresh-interval` (known concern in [futureideas.md](../../planning/futureideas.md)).
- Vault not listed in Obsidian: `tbuffet open` refuses before launching.
