# Implementation in Token Buffet

How the [plugin](plugin-capabilities.md) is wired to the router, and how the demo vaults were made. Files live in `src/tokenbuffet/default_templates/` (copied into a workspace by `tbuffet init` / `tbuffet demo init`).

## Config cascade

Same file set at each layer (see [app_configuration.md](../app_configuration.md)):

```
integrations/obsidian/             app type
registered_apps/obsidian/<name>/   one registered vault (its app_config.json carries path and vault_type)
```

| File | Role |
|---|---|
| `app_config.json` | Endpoint, `model_mode`, `task_model_tiers`, `vault_type`, `bridge_configuration` (the `data.json` path) |
| `app_settings.json` | Base plugin settings and automation defaults |
| `vault_types.json` | Presets merged over the base: `default`, `finance-conference`, `research-papers`, `daily-notes` |
| `configure.py` | Builds `data.json` |
| `init.py` | Hooks (below) |

`configure.py` merges, in order: `app_settings.json`, the `vault_types.json` preset, then the router settings from `app_config.json -> client_settings`. It writes `<vault>/.obsidian/plugins/karpathywiki/data.json` and keeps keys it does not own. `tbuffet reconfigure-app obsidian <name>` re-applies it.

## Settings Token Buffet writes

| Plugin key | Value | Why |
|---|---|---|
| `provider` | `custom-responses` | Calls the router's OpenAI Responses endpoint |
| `baseUrl` | `http://127.0.0.1:8090/v1/` | Router root; no per-client route |
| `apiKey` | `TokenBuffet` | Placeholder; the router needs no key |
| `model`, `availableModels` | `fast`; `fast` / `medium` / `reasoning` | A "model" is a router tier |
| `usePerTaskModels` | `true` | Different tier per task |
| `ingestModel` / `lintModel` / `queryModel` | `fast` / `reasoning` / `reasoning` | Cheap extraction vs judgment |
| `disableThinking` | `true` | Avoids extended-thinking overhead on the CLI backends |

The plugin falls back to the `apiKey` in `data.json` when its SecretStorage entry is empty, so no secret is written.

## Vault types

A vault type is a tag vocabulary plus query instructions; nothing else differs.

| Vault type | Entity tags | Concept tags |
|---|---|---|
| `default` | plugin defaults | plugin defaults |
| `finance-conference` | person, organization, fund, asset_class, instrument, index, other | financial_strategy, portfolio_archetype, action_playbook, theory, terminology |
| `research-papers` | author, institution, dataset, method, metric, venue, other | research_contribution, technique, theory, benchmark, open_problem, terminology |
| `daily-notes` | person, project, place, organization, topic, other | idea, decision, task, question, reference, terminology |

A new vault type is a new key in `vault_types.json`; no engine change.

## `init.py` hooks

| Hook | Used by | Does |
|---|---|---|
| `check()` | `add-app`, `doctor`, dashboard | Raises if Obsidian's settings folder is missing, which hides the app type |
| `link(app_path)` | `tbuffet demo init`, `launch()` | Adds the vault to Obsidian's `obsidian.json` and returns its vault id |
| `launch(app_path)` | `tbuffet open`, dashboard Open button | Opens `obsidian://open?vault=<id>` |
| `prepare_demo(app_path)` | `tbuffet demo init` | Writes Obsidian's `enable-plugin-<vault id>` trust entry into its localStorage LevelDB log (Obsidian must be closed) |
| `init(app_path)` | app initialization | Creates `_Inbox/` |

## Register your own vault

```bash
tbuffet add-app obsidian my-vault --path "/path/to/vault" --vault-type research-papers
tbuffet reconfigure-app obsidian my-vault
tbuffet open obsidian my-vault
```

The plugin itself must be installed in the vault (Settings > Community plugins > "Karpathy LLM Wiki"); Token Buffet only writes its settings.

## Demo vaults

`demo/Obsidian-LLM-Wiki/` ships two finished vaults, so the graph, index and Query panel work immediately.

| Vault | Source material | Vault type | `_Inbox` notes | Wiki pages |
|---|---|---|---|---|
| `conference-notes` | Masked notes from a tax and wealth-management conference (dates and attendee names anonymized) | `finance-conference` | 10 | 10 sources, 90 entities, 171 concepts |
| `daily-notes` | Weeknotes from [Simon Willison's blog](https://simonwillison.net/), with attribution | `daily-notes` | 28 | 28 sources, 232 entities, 106 concepts |

Each ships the plugin files, a `data.json` with `llmReady: true`, Obsidian core config (`app.json`, `graph.json`, `bookmarks.json`, ...) and its `wiki/`.

### How the demos were built

1. **Ingestion with an LLM.** Source notes were placed in `_Inbox/` and ingested through the plugin against the router on the `fast` tier. The plugin's `wiki/log.md` records each run (a 17 KB weeknote took 950 s; a 22 KB conference keynote took 347 s) and produced the `sources/`, `entities/` and `concepts/` pages, `index.md` and `log.md`.
2. **Synthesis with LLMs.** The ingested wiki was then synthesized further with LLMs into the finished state that ships.
3. **Vault-type tuning.** The `finance-conference` and `daily-notes` presets were written so extraction matched each corpus: strategies and playbooks for the conference; people, projects and ideas for the journal.
4. **Packaging.** The vaults were copied into `default_templates/demo/` and their registrations into `default_templates/registered_apps/obsidian/`.

> To fill in: which models and tiers the synthesis step used, and what drove it. `wiki/log.md` records only ingest runs, so step 2 cannot be reconstructed from the repo.

Doc drift to fix: `demo/Obsidian-LLM-Wiki/README.md` and the two vault READMEs still say 427 and 275 notes; the vaults contain 10 and 28 source notes.

### Running a demo

1. Enable **Settings > General > Command line interface** in Obsidian (only `tbuffet open` needs it).
2. `tbuffet demo init` copies the demos, then per Obsidian demo calls `link()` and `prepare_demo()`. Obsidian must be closed; no router needs to be running. Setup writes `llmReady: true` directly, so there is no connection test.
3. `tbuffet start`.
4. `tbuffet open obsidian conference-notes` (or `daily-notes`). Drop a note into `_Inbox/`, or run Query, Lint or Ingest from the command palette.
