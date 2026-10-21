---
type: source
created: 2026-10-21
updated: 2026-10-21
tags: [other]
aliases:
  - "2023-09-17-weeknotes-embeddings"
  - "Weeknotes: Embeddings"
  - "more embeddings and Datasette Cloud"
contentHash: 45aa-c96f290a
source_file: "[[_Inbox/2023-09-17-weeknotes-embeddings.md]]"
generation_complete: true
---

# 2023-09-17-weeknotes-embeddings - Summary

## Source

- Original file: [[_Inbox/2023-09-17-weeknotes-embeddings.md]]
- Ingested: 2026-10-21

## Core Content

Simon Willison's weeknotes for 17 September 2023 cover a burst of work on [[entities/llm|LLM]], [[entities/datasette|Datasette]] and [[entities/datasette-cloud|Datasette Cloud]]. LLM gained [[concepts/embeddings|embedding]] support in versions 0.9 and 0.10, and plugins such as [[entities/llm-clip|llm-clip]], [[entities/llm-cluster|llm-cluster]] and [[entities/datasette-llm-embed|datasette-llm-embed]] extend it to image search, clustering and SQL. Datasette Cloud runs on the Datasette 1.0 alpha series, and its use drove many plugin releases, including a new `actors_from_ids` plugin hook built with [[entities/alex-garcia|Alex Garcia]] for social features.

The post's central thread is a data-integrity problem. A [[entities/sqlite-utils|sqlite-utils]] bug rewrote the [[concepts/rowid|rowid]] column and broke [[concepts/full-text-search|full-text search]] on Datasette Cloud. Willison then learned that SQLite rowid values are unstable because they change on VACUUM. This led him to design [[entities/sqlite-chronicle|sqlite-chronicle]], which uses triggers to build a [[concepts/chronicle-table|chronicle table]] so external systems can sync only changed rows. The post closes with TILs on [[entities/hugging-face|Hugging Face]] hosting, [[entities/claude|Claude]] summarization and [[entities/cr-sqlite|cr-sqlite]].

## Key Entities

- [[entities/llm|LLM]] — command-line tool for language models, gaining embedding support
- [[entities/datasette|Datasette]] — open source tool for exploring and publishing data built on SQLite
- [[entities/datasette-cloud|Datasette Cloud]] — hosted Datasette service that drove ecosystem improvements
- [[entities/sqlite-utils|sqlite-utils]] — Python library and CLI for manipulating SQLite databases
- [[entities/sqlite-chronicle|sqlite-chronicle]] — trigger-based change-tracking for SQLite tables
- [[entities/alex-garcia|Alex Garcia]] — developer building Datasette Cloud features
- [[entities/clip|CLIP]] — image and text embedding model
- [[entities/llm-clip|llm-clip]] — LLM plugin generating CLIP embeddings
- [[entities/llm-cluster|llm-cluster]] — LLM plugin for clustering embeddings and naming clusters
- [[entities/datasette-llm-embed|datasette-llm-embed]] — Datasette plugin adding an `llm_embed` SQL function
- [[entities/symbex|Symbex]] — tool for extracting Python symbols for embedding workflows
- [[entities/blip-caption|blip-caption]] — CLI tool wrapping the Salesforce BLIP captioning model
- [[entities/salesforce-blip|Salesforce BLIP]] — image captioning model
- [[entities/hugging-face|Hugging Face]] — hosts machine learning models and demo hosting
- [[entities/claude|Claude]] — Anthropic's large language model, accessed through an API
- [[entities/fly-io|Fly.io]] — hosting company sponsoring Alex Garcia's Datasette Cloud work
- [[entities/datasette-write-ui|datasette-write-ui]] — plugin for inserting, editing and deleting table rows
- [[entities/datasette-edit-schema|datasette-edit-schema]] — plugin for editing table schemas
- [[entities/sqlite-migrate|sqlite-migrate]] — migration system for SQLite, used to manage LLM's embedding schema
- [[entities/datasette-auth-tokens|datasette-auth-tokens]] — plugin for API token authentication
- [[entities/datasette-short-links|datasette-short-links]] — experimental link shortener for Datasette
- [[entities/cr-sqlite|cr-sqlite]] — extension adding CRDT support to SQLite

## Key Concepts

- [[concepts/embeddings|embeddings]] — vector representations capturing semantic meaning
- [[concepts/semantic-search|semantic search]] — finding content by meaning rather than keywords
- [[concepts/rowid|rowid]] — SQLite's internal row identifier, shown to be unstable
- [[concepts/chronicle-table|chronicle table]] — shadow table recording row inserts, updates and deletions
- [[concepts/database-backed-access-tokens|database-backed access tokens]] — revocable tokens that record last use
- [[concepts/llama-cpp-python-grammars|llama-cpp grammars]] — constrained output formats for local models
- [[concepts/openai-functions|OpenAI Functions]] — structured function-call output from the OpenAI API, used as a benchmark
- [[concepts/full-text-search|full-text search]] — keyword indexing of text columns in a database
- [[concepts/crdt|CRDT]] — conflict-free replicated data types enabling merged independent writes

## Main Points

- LLM gained embedding support in version 0.9 and binary CLIP embedding support in version 0.10, enabling plugins for image search, clustering and SQL-based embeddings.
- Datasette Cloud, running on the Datasette 1.0 alpha series, exposed breaking changes that drove many plugin releases and a new `actors_from_ids` plugin hook.
- A sqlite-utils bug rewrote the rowid column and broke full-text search, revealing that SQLite rowid values are unstable across VACUUM operations.
- sqlite-chronicle uses triggers to create a lightweight chronicle table, letting external processes sync only rows changed since their last version.
- Willison plans Retrieval Augmented Generation support for LLM and Datasette, built on the existing embedding mechanism.

## Mentions in Source

- "I always include a list of new releases in my weeknotes." — [[_Inbox/2023-09-17-weeknotes-embeddings|2023-09-17-weeknotes-embeddings]]
- "I ended up building this tiny little CLI tool that wraps the model:" — [[_Inbox/2023-09-17-weeknotes-embeddings|2023-09-17-weeknotes-embeddings]]
- "I built [sqlite-history](https://simonwillison.net/2023/Apr/15/sqlite-history/) a few months ago, which uses SQLite triggers to create a full copy of the updated data every time a row in a table is edited." — [[_Inbox/2023-09-17-weeknotes-embeddings|2023-09-17-weeknotes-embeddings]]
- "[Alex Garcia](https://alexgarcia.xyz/) has been working with me building out features for Datasette Cloud, generously sponsored by [Fly.io](https://fly.io/)." — [[_Inbox/2023-09-17-weeknotes-embeddings|2023-09-17-weeknotes-embeddings]]
- "Alex is using this in `datasette-short-links`, and I built two plugins to work with the new hook as well:" — [[_Inbox/2023-09-17-weeknotes-embeddings|2023-09-17-weeknotes-embeddings]]
- "Datasette Cloud lets users insert, edit and delete rows from their tables, using the plugin Alex built called [datasette-write-ui](https://github.com/datasette/datasette-write-ui) which he [introduced on the Datasette Cloud blog](https://www.datasette.cloud/blog/2023/datasette-write-ui/)." — [[_Inbox/2023-09-17-weeknotes-embeddings|2023-09-17-weeknotes-embeddings]]
- "[Datasette Cloud](https://www.datasette.cloud/) continues to drive improvements to the wider Datasette ecosystem as a whole." — [[_Inbox/2023-09-17-weeknotes-embeddings|2023-09-17-weeknotes-embeddings]]
- "It runs on the latest Datasette 1.0 alpha series, taking advantage of [the JSON write API](https://simonwillison.net/2022/Dec/2/datasette-write-api/)." — [[_Inbox/2023-09-17-weeknotes-embeddings|2023-09-17-weeknotes-embeddings]]