# Obsidian LLM Wiki (Karpathy LLM Wiki plugin)

Token Buffet's flagship knowledge integration. It points the **Karpathy LLM Wiki** Obsidian plugin (`karpathywiki`) at the Token Buffet router, so the plugin's ingest, lint and query work runs on your flat-rate CLI subscriptions (Claude, Codex, Grok, agy) instead of a paid API.

| Document | What it covers |
|---|---|
| **README.md** (this file) | Index and the one-paragraph summary |
| [pattern.md](pattern.md) | The Karpathy LLM Wiki pattern itself, independent of any tool |
| [architecture.md](architecture.md) | End-to-end flow and which layer owns what |
| [plugin-capabilities.md](plugin-capabilities.md) | What the `karpathywiki` plugin can do: commands, ingest/query/lint pipelines, settings, limits |
| [implementation.md](implementation.md) | How Token Buffet implements it: config cascade, settings written, hooks, demo vaults and how they were built |
| [graphify-and-data-views.md](graphify-and-data-views.md) | Planned expansion: graph visualization and data views |

## In one paragraph

Karpathy's pattern replaces query-time retrieval (RAG) with an LLM that continuously **compiles** raw notes into a persistent, interlinked markdown wiki. The `karpathywiki` plugin implements that pattern inside Obsidian. Token Buffet supplies the LLM: the plugin is configured to call the local router, which maps its per-task model tiers (`fast` for ingest, `reasoning` for lint and query) onto whichever CLI subscription has quota left.

```
raw notes -> plugin (ingest) -> wiki/ pages <- plugin (query, lint)
                  |                                   |
                  +------ router :8090 /v1/responses -+--> CLI subscriptions
```

## Sources

- [Karpathy's LLM Wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) (the pattern)
- [Plugin page](https://community.obsidian.md/plugins/karpathywiki) and [plugin repo](https://github.com/GD4AI/obsidian-llm-wiki) (v1.29.0 at the time of writing; the demo vaults ship v1.28.0)
