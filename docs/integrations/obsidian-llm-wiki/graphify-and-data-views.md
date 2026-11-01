# Planned: Graphify and data views

Status: **not started**. This page records the intended design and the open questions.

## Principle: build on top of the wiki, do not re-ingest

The LLM Wiki plugin has already done ingestion: raw notes became `wiki/sources/`, `wiki/entities/` and `wiki/concepts/` (see [pattern.md](pattern.md), [plugin-capabilities.md](plugin-capabilities.md)). Graphify is a **second stage on top of that finished wiki**.

- It does **not** read `_Inbox/` or `wiki/sources/`, and it does not run the plugin's ingest again.
- Its only input is **`wiki/entities/` and `wiki/concepts/`**: the already-extracted nodes, with their frontmatter and `[[wikilinks]]`.
- It **enhances** that layer further, instead of producing a parallel extraction.

```
raw notes -> plugin ingest -> wiki/sources + entities + concepts      (done, as today)
                                          |
                                          v  read entities/ + concepts/ only
                                      graphify  -> enhanced graph + data views
```

Provenance still works without reading `sources/`: each entity and concept page already lists its source pages in its `sources:` frontmatter and in **Mentions in Source**, so lineage can be shown without opening source pages.

Related: the roadmap lists "Graphify with Obsidian Docs" ([futureideas.md](../../planning/futureideas.md)). `CLAUDE.md` calls `graphify/` a separate graph-only second-brain sub-project, but that folder is not in this repo. Claudia's `/brain` 3D visualizer is also called "graphify" ([claudia_integration.md](../claudia_integration.md)); whether these are the same thing is undecided.

## Input: what an entity or concept page gives

| Field | Gives |
|---|---|
| File path | Node id and node class (`entities/` vs `concepts/`) |
| Frontmatter `tags` | Node subtype from the vault's tag vocabulary (e.g. `person`, `financial_strategy`) |
| Frontmatter `aliases` | Alternate names, for matching and search |
| Frontmatter `sources`, `created`, `updated` | Lineage and time |
| `Related Entities` / `Related Concepts` sections and body `[[wikilinks]]` | Edges |
| Description text | One-paragraph summary per node |
| `reviewed: true` | Human-verified marker |

Current size: conference-notes 90 entities + 171 concepts, daily-notes 232 entities + 106 concepts, so each vault fits in one in-memory graph.

## Enhancement (what "further" adds)

Open: the plugin's edges are untyped wikilinks. Candidate enhancements, to be chosen:

- **Typed edges**: classify each link (e.g. uses, part-of, contradicts, example-of) with an LLM call per node neighborhood.
- **Clustering and hubs**: communities, central nodes, bridges between clusters.
- **Cross-vault linking**: match entities/concepts across vaults by alias.
- **Enhanced node summaries** derived from the Description sections.

Any LLM step here runs through the router like everything else; the tier (likely `reasoning`) is a decision to make. Enhancement output must be stored **outside** `wiki/entities/` and `wiki/concepts/` (the plugin owns those files and rewrites them on ingest and Smart Fix); where it lives is open.

## Data views

Views over the same input plus the enhancement output:

- **Nodes table**: type, tags, aliases, source count, last updated; filterable by tag vocabulary.
- **Neighborhood**: a node and its linked entities and concepts.
- **Graph health**: orphans, dead links, untagged pages (read-only versions of the checks lint already runs).
- **Per-source lineage**: pick an entity or concept, list the sources it came from.

Optional operational views, from files outside this principle's input: `wiki/log.md` (ingest durations and counts) and router request records (cost per operation).

## Open decisions

- **Where it lives**: Obsidian-side only (graph view config), a dashboard tab (`TAB_PATHS` in `app.js` plus a `STATIC_FILES` route in `server.py`), or the separate `graphify/` project.
- **Cache**: parse the markdown on demand, or write a derived JSON export under `data/` (gitignored) refreshed after each ingest.
- **Write-back**: read-only, or allowed to change vault files (e.g. set `reviewed: true`).
- **Obsidian deep links**: `obsidian://open?vault=<id>&file=<path>` from the graph; the `file` parameter is unverified, check the Obsidian URI docs before building on it.
- **Obsidian-native tooling** (Bases, community plugins) may cover part of the data views; unverified, check current docs first.

## Constraints from the repo

- Config-driven: a new view or enhancement is data (config or export schema), not an Obsidian-specific branch in the engine.
- All services bind to `127.0.0.1` via `tokenbuffet/loopback.py`.
- New dashboard tabs need both `TAB_PATHS` and `STATIC_FILES` entries.
- First MVP build: no backward-compatibility shims.
