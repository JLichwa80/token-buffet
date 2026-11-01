# Plugin capabilities (`karpathywiki`)

The plugin is the [Karpathy LLM Wiki](https://community.obsidian.md/plugins/karpathywiki) community plugin for Obsidian (Apache-2.0, plugin id `karpathywiki`, Obsidian 1.11.4+, desktop and mobile). It implements the [pattern](pattern.md) with no backend, no telemetry and no embeddings. It only creates new pages under `wiki/`; source notes are read-only. Facts here are from the plugin page and repo (v1.29.0); the demo vaults ship v1.28.0.

## Wiki structure

| Path | Contents |
|---|---|
| `wiki/sources/` | One page per ingested note: summary, key entities, key concepts, provenance link back to the note |
| `wiki/entities/` | Named things: people, organizations, products, projects, events |
| `wiki/concepts/` | Topics, methods, theories, terms, decisions |
| `wiki/schema/config.md` | The editable vocabulary and page templates the LLM must follow |
| `wiki/index.md` | Auto-generated directory of every page with its aliases |
| `wiki/log.md` | Auto-generated operation log |

Every page has frontmatter (`type`, `created`, `updated`, `tags`, `aliases`, `sources`). Entity and concept pages end with a **Mentions in Source** section of verbatim quotes. `reviewed: true` marks a page human-verified and protects it from overwrite.

## Commands (command palette)

| Command | What it does |
|---|---|
| Ingest single source | One Markdown or PDF note |
| Ingest from folder | Batch-ingest a folder, with Smart Batch Skip for files already ingested |
| Ingest multiple files | Pick a subset in a two-pane file tree, with a live queue and per-file cancel |
| Query wiki | Chat in a right-docked panel; answers cite `[[wiki-links]]` |
| Lint wiki | Health scan: duplicates, dead links, empty pages, orphans, missing aliases, contradictions |
| Smart Fix All | Button in the lint modal; repairs in order: fill aliases, merge duplicates, fix dead links, link orphans, expand empty pages |
| Regenerate index | Rebuilds `wiki/index.md` |
| Cancel current ingestion | Stops at the next batch boundary (also from the status bar) |
| View operation history | Searchable record of ingests, lint reports and maintenance runs |
| Recreate Wiki Welcome Note | Re-creates the welcome note in the current wiki language |

Ribbon icons: a sticker ingests the active note, a message-circle opens Query.

## Ingest pipeline

```
note in _Inbox/
  -> pre-ingest gate (empty / frontmatter-only rejected; content-hash dedup)
  -> LLM extraction: entities + concepts at the configured granularity
  -> candidate gate (skipMentionOnlyCandidates, gateDissentStubs) -> pages or stubs
  -> page generation, up to pageGenerationConcurrency (5) in parallel
  -> smart merge into existing pages (aliases kept, contradictions flagged)
  -> tags checked against the tag vocabulary (outside values dropped)
  -> write sources/<note>_<hash>.md, entities/*.md, concepts/*.md
  -> update index.md, append to log.md
```

- Every page gets at least one alias (drives cross-language duplicate detection).
- Slugs are lower-case (`slugCase: lower`); source page names get a short content-hash suffix.
- A source page records `source_file`, `contentHash` and the ingest date, so every entity and concept traces back to its note.
- One note fans out into several LLM requests. In the demo logs, `fast`-tier ingests took 150 s to 1150 s per note.
- `log.md` entries: `## [date time] ingest | <note> · <seconds>s · <tier> · <size>KB`, then created and updated page lists.

## Query pipeline

A five-stage seed-selection cascade that stops early when a stage has enough signal:

1. BM25F over titles, aliases, summaries and bodies
2. LLM keyword generation (8-12 keywords)
3. Local substring scan of the keywords (no LLM call)
4. LLM fallback pass over the wiki when lexical signals are weak
5. Monte Carlo Personalized PageRank (3,000 walks x 50 steps) over `[[wiki-link]]` edges, for multi-hop context

The selected pages are given to the model along with `customQueryInstructions`; the answer cites `[[wiki-links]]`. Answer budget 16,000 tokens. The wikilink graph is the search index, so hand-added links are picked up by the next query.

## Lint and Smart Fix All

Duplicate detection is tiered: direct name matches, then shared-link and bigram similarity (`lintJaccardLinkThreshold`, `lintJaccardBodyGate`, `lintBigramThreshold`). Other checks: dead links, empty pages, orphans, missing aliases, contradictions. `createStubsForUnresolvableLinks` controls whether dead links get stub pages. Lint can run on a schedule (`periodicLint`) and fix automatically (`autoSmartFix`).

## Settings by area

| Area | Keys |
|---|---|
| Provider | `provider`, `baseUrl`, `apiKey`, `model`, `availableModels` |
| Per-task models | `usePerTaskModels`, `ingestModel`, `lintModel`, `queryModel` (and `*UseCustom`) |
| Vocabulary | `tagVocabularyMode`, `customEntityTags`, `customConceptTags`, `enableSchema` |
| Extraction | `extractionGranularity`, `extractionTemperature`, `skipMentionOnlyCandidates`, `gateDissentStubs` |
| Query | `customQueryInstructions`, `chatTemperature`, `maxConversationHistory` |
| Automation | `autoWatchSources`, `autoWatchMode`, `watchedFolders`, `autoWatchDebounceMs`, `periodicLint`, `startupCheck`, `autoSmartFix` |
| Throughput | `pageGenerationConcurrency`, `batchDelayMs`, `maxTokensPerCall`, `disableThinking` |
| Output | `wikiFolder`, `wikiLanguage`, `language`, `slugCase` |

The plugin supports 11 UI languages and 11 wiki-output languages, chosen independently.

## Providers the plugin supports

16+ providers: Anthropic, OpenAI, Google Gemini, DeepSeek, Alibaba Qwen, xAI Grok, Moonshot Kimi, Zhipu GLM, MiniMax, Step, Tencent Hunyuan, Xiaomi MiMo, Google Gemma, AWS Bedrock, ChatGPT Plan (Codex OAuth, experimental), plus Ollama, LM Studio, OpenRouter, Anthropic-Compatible and Custom OpenAI-Compatible. Token Buffet uses the **Custom OpenAI Responses** variant (`custom-responses`).

## Documents beyond Markdown

The plugin can also ingest PDFs (native on Anthropic, OpenAI, Gemini, Bedrock; or via its MinerU backend), images and Office files (via MinerU), and can analyze embedded images. **Token Buffet does not use these paths:** the proxy flattens requests to text, so images and PDFs would be dropped. See the multimodal proposal in [futureideas.md](../../planning/futureideas.md).

## Limits

- Answers come only from the vault, not the web.
- Small models occasionally return the built-in tag taxonomy instead of the vault's; the plugin drops those tags and lint reports untagged pages.
- Large vaults need long-context models (the plugin recommends 200K+ tokens above roughly 500 pages).
- Benchmark and quality claims on the plugin page are self-reported.
