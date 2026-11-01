# The Karpathy LLM Wiki pattern

Source: [Andrej Karpathy's "LLM Wiki" gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f). The gist is an "idea file": it is meant to be pasted into an LLM agent, which then builds a concrete version with you. It is intentionally abstract; directory layout, schema, page formats and tooling are left to you and your LLM. Everything on this page except the last section comes from the gist.

## The problem with RAG

Most LLM document tools retrieve relevant chunks at query time and answer from scratch each time. The gist's complaint: "the LLM is rediscovering knowledge from scratch on every question." Nothing accumulates, and a question that needs five documents synthesized has to re-synthesize them every time.

## The idea

Have the LLM **incrementally build and maintain a persistent wiki**: a set of interlinked markdown files that sits between you and your raw sources. When a new source arrives, the LLM does not just index it; it integrates it into the existing pages (updating entities, revising summaries, flagging contradictions). The wiki is "a persistent, compounding artifact", and you rarely write it yourself.

> Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase.

## Why it works

"The tedious part of maintaining a knowledge base is... the bookkeeping": updating cross-references, keeping summaries current, noting where new data contradicts old claims. Humans abandon wikis because maintenance grows faster than value. LLMs do not get bored, so the cost of maintenance is near zero. You curate sources and ask questions; the LLM does the rest. The gist ties this to Vannevar Bush's 1945 Memex: the LLM supplies the maintenance Bush could not.

## Three layers

| Layer | Owner | Contents |
|---|---|---|
| **Raw sources** | You | Curated, immutable documents (articles, papers, images, data). The source of truth; the LLM reads but never modifies them |
| **The wiki** | The LLM | Generated markdown: summaries, entity pages, concept pages, comparisons, an overview. You read it; the LLM writes it |
| **The schema** | You and the LLM, together | A config document (the gist names `CLAUDE.md` / `AGENTS.md`) defining structure, conventions and workflows. Refined over time |

## Three operations

- **Ingest.** You add a source. The LLM reads it, discusses takeaways, writes a summary page, updates the index, revises related pages (one source may touch 10 to 15 pages) and appends to the log. Karpathy prefers ingesting one source at a time, supervised.
- **Query.** The LLM searches the wiki and synthesizes an answer with citations. Output can be markdown, a table, slides (Marp) or a chart. Good answers can be **filed back into the wiki**, so explorations compound like ingested sources do.
- **Lint.** Periodic health checks: contradictions, stale claims, orphan pages, missing concept pages, missing cross-references, data gaps.

## Two special files

- **`index.md`**: content-oriented catalog of every page with a link and one-line summary, organized by category. The LLM reads it first when answering. The gist reports this works "surprisingly well" at about 100 sources and a few hundred pages, with no embedding infrastructure.
- **`log.md`**: chronological, append-only record with consistent prefixes such as `## [2026-04-02] ingest | Article Title`, so simple Unix tools can parse it.

## Tooling the gist mentions (all optional)

- A local search tool such as qmd (hybrid BM25/vector, CLI and MCP) once the wiki outgrows the index.
- Obsidian Web Clipper to turn web articles into markdown sources.
- Downloading images locally so the LLM can reference them (it reads the text first, then views images separately).
- Obsidian graph view to spot hubs and orphans; Marp for slide decks; Dataview to query YAML frontmatter.
- The wiki is just a git repo of markdown files, which gives history and collaboration.

## Use cases the gist lists

Personal tracking (goals, health, journaling), deep research, reading a book (character and theme pages, fan-wiki style), business and team wikis fed by Slack and meetings, due diligence, trip planning, course notes, hobby research.

## How the pieces map to this repo

| Pattern element | In the plugin | In Token Buffet |
|---|---|---|
| Raw sources | Notes in the vault, e.g. `_Inbox/` (never modified) | Demo `_Inbox/` folders |
| Wiki | `wiki/sources`, `wiki/entities`, `wiki/concepts` | Shipped pre-built in the demo vaults |
| Schema | `wiki/schema/config.md` plus the tag vocabulary settings | Per-vault `vault_types.json` presets |
| `index.md` / `log.md` | Auto-generated, same names | Log is the record of how the demos were ingested |
| Ingest / query / lint | Commands and auto-watch | Run on the router tiers `fast` / `reasoning` / `reasoning` |
| LLM | Provider setting | The local router, backed by CLI subscriptions |

Differences from the gist as written: the plugin does retrieval with BM25F plus a graph walk (Personalized PageRank over `[[wiki-links]]`), not by having the LLM read `index.md` first, and it enforces the schema through a controlled tag vocabulary. Details in [plugin-capabilities.md](plugin-capabilities.md).
