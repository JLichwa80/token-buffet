---
type: entity
created: 2026-10-21
updated: 2026-10-21
generation_complete: true
sources:
  - "[[sources/2023-12-31-weeknotes_456c53]]"
  - "[[sources/2023-12-08-weeknotes_cbd558]]"
  - "[[sources/2023-11-22-weeknotes_49168f]]"
  - "[[sources/2023-10-30-weeknotes_d4a215]]"
  - "[[sources/2023-10-22-weeknotes_1435b6]]"
  - "[[sources/2023-09-17-weeknotes-embeddings_c2332f]]"
  - "[[sources/2023-08-30-datasette-plus-weeknotes_748a0c]]"
  - "[[sources/2023-08-16-datasette-cloud-weeknotes_9ee111]]"
  - "[[sources/2023-08-05-weeknotes-plugins_fc2660]]"
  - "[[sources/2023-07-16-weeknotes_8e11f0]]"
  - "[[sources/2023-06-27-weeknotes_f6a59b]]"
  - "[[sources/2023-05-01-weeknotes_72fe7e]]"
  - "[[sources/2023-03-22-weeknotes_1bbf6a]]"
  - "[[sources/2023-02-09-weeknotes_05bd6f]]"
  - "[[sources/2023-01-15-weeknotes_aefc7f]]"
tags:
  - "other"
  - "project"
aliases:
  - "Datasette project"
---

# Datasette

## Description

Datasette is an open source multi-tool for exploring and publishing data, and it is the central project in the [[sources/2023-12-31-weeknotes_456c53|2023-12-31 weeknotes]]. The post lists several Datasette releases and plugins, including datasette 0.64.6 released on 2023-12-22 and [[datasette-haversine]] 0.2.1. Its plugin ecosystem is a recurring theme: [[datasette-plot]], [[datasette-sqlite-authorizer]], and [[datasette-haversine]] all extend it. The release list shows Datasette as a base for many of the author's other data tools. [[Datasette Cloud]], the hosted offering that [[Alex Garcia]]'s plugin was built around, is closely tied to it.

Datasette's extensibility is also shown by the Datasette Enrichments framework, described as the biggest new Datasette feature in some time and implemented entirely as a plugin, which lets plugins run transformations or data fetches against selected rows, such as geocoding addresses, executing a GPT prompt, or applying a regular expression. [[Alex Garcia]] released the first version of datasette-comments, which lets users leave comments on individual rows so they can collaborate on finding stories in data, adding to his work on [[Datasette Cloud]]. datasette-chronicle adds table actions to enable or disable chronicle tracking for users with the right permissions, plus a `?_since=VERSION` querystring parameter that filters tracked tables to rows changed since a given version, and it is built on sqlite-chronicle.

Enrichments also supports OCR and language model prompts, and Simon Willison began building the first working version in November 2023. The plugin ecosystem includes datasette-sentry and datasette-edit-schema alongside datasette-comments and datasette-enrichments. In November 2023, after attending OpenAI DevDay and the year's conferences, Willison spent a week working with [[Alex Garcia]] on [[Datasette Cloud]].

Datasette Cloud is being iterated on based on feedback from people using its preview, as of October 2023. [[datasette-edit-schema]] 0.7 adds the ability to add and remove indexes on larger tables to speed up faceting, a feature requested by [[Datasette Cloud]] preview users.

Datasette is being prepared for a 1.0 release, and [[Alex Garcia]] is cleaning up its metadata system by moving permissions, allow blocks, canned queries, and other non-metadata settings out of metadata into a separate `datasette.yaml` (or `datasette.json`) configuration file.

Datasette Cloud runs on the latest 1.0 alpha series and takes advantage of the JSON write API. Its API uses database-backed access tokens, so users can revoke them, and each token records when it was last used; this is built into the datasette-auth-tokens plugin. The 1.0 alpha series introduced breaking changes that caused older plugins to fail, which Datasette Cloud exposed. Because Datasette does not dictate the shape of actor representations, a new `actors_from_ids` plugin hook was built with [[Alex Garcia]] to resolve actor IDs shown in lists to their names for social features. Simon Willison is also designing future Datasette features on the assumption that `rowid` is a useful stable identifier for a row.

Datasette 1.0a4 patched CVE-2023-40570, in which the API explorer exposed database and table names to unauthenticated users. Datasette 1.0a5 added a `--setting` option that expresses any configuration as command-line key/value pairs, and an `--actor` option for `datasette --get`. In 1.0a5, the `_internal` database was also reworked, driven by Datasette Cloud work: it no longer appears in `datasette.databases` by default and is available to plugins through `datasette.get_internal_database()`, with a new `--internal` option to persist it to disk, so plugins can store tokens and progress data that stays hidden from users. Simon Willison uses `datasette --get` to generate social media card images for his TILs site, simulating HTTP requests without starting a server.

Datasette 1.0 is the first version that will be marked as "stable", with the aim of guaranteeing that software built on it won't break before Datasette 2.0. The stable commitments are a stable plugins interface, a stable JSON API format, and stable template contexts. The Datasette 1.0 alpha 3 release, published 9 August 2023, focused mainly on JSON support, including a new, more intuitive default JSON shape for both table and arbitrary query pages.

The 1.0 alphas introduced a write API, and the author built a mechanism into the existing datasette-auth-tokens plugin (released in preview as 0.4a0) so [[Datasette Cloud]] users can set up automatic imports of data into their instances through that API.

Datasette is an open source tool for exploring and publishing SQLite databases, which Simon Willison develops, and its website hosts a growing collection of tutorials. Willison chose that site as the permanent home for his Data analysis with SQLite and Python tutorial, which now includes the full 2hr45m video and an improved written handout.

Simon Willison's LLM command-line tool, documented at llm.datasette.io, uses a plugin architecture described as "inspired by plugins in Datasette," so Datasette's plugin system also served as a design model beyond its own ecosystem.

Datasette's redesigned default JSON format replaces the older one, which had dozens of keys and returned row data as arrays. The new format is a simpler object with `ok`, `next`, and `rows` keys, and optional extras are requested with an `_extra` parameter. Simon Willison also runs his own Datasette instance over a SQLite copy of his blog, and an Observable newsletter notebook queries that instance.

Datasette 0.64 added the `--setting default_allow_sql off` option, because some SQL functions added by the SpatiaLite module could crash a Datasette instance. Simon Willison also built an experiment that used custom SQL functions inside Datasette to create a question-and-answer interface over a document corpus, exposing OpenAI API calls and vector search as SQL functions. That work produced the datasette-openai, datasette-faiss, datasette-cookies-for-magic-parameters, and openai-to-sqlite releases.
## Related Entities

- [[entities/datasette-cloud|datasette-cloud]]
- [[entities/datasette-plot|datasette-plot]]
- [[entities/alex-garcia|Alex Garcia]]
- [[entities/django-sql-dashboard|Django SQL Dashboard]]
- [[entities/sqlite-utils-shell|sqlite-utils-shell]]
- Alex Garcia wrote [[entities/datasette-write-ui|datasette-write-ui]], a Datasette plugin that adds a user interface for editing, inserting, and deleting rows. He also worked with Simon Willison to prepare [[entities/datasette-cloud|datasette-cloud]] for general availability, with Fly.io supporting that work.
dclient 0.2 added a `dclient insert` command that reads CSV, TSV, or JSON data and writes it to an external Datasette instance through the Datasette 1.0 write API.
datasette-render-markdown 2.2 (July 2023) added a custom Jinja block tag and an automatically generated table of contents built from the page's HTML headers. The July 2023 weeknotes also list datasette-upload-csvs in the Datasette plugin release list.
[[entities/datasette-lite|Datasette Lite]] is a related Datasette-based project that runs Python in the browser through WebAssembly.
## Related Concepts

- [[concepts/plugins|plugin system]]
- Datasette plugin releases driven by Datasette Cloud in September 2023 include datasette-export-notebook 1.0.1, datasette-cluster-map 0.18a0, datasette-graphql 3.0a0 (automatic GraphQL API for SQLite databases), datasette-auth-tokens 0.4a3, and datasette-llm-embed 0.1a0 (adds an `llm_embed(model_id, text)` SQL function).
- Cameron Yick contributed a JavaScript plugin API that lets plugins modify the Datasette interface, adding custom panels above the main table view (shown as tabs when several plugins use the area) and extra options in the column cog action menu.
- datasette-render-images 0.4 (released 2023-06-14): Datasette plugin that renders binary blob images using data-uris.
- Datasette 0.64.2 was among the recent releases listed in the March 2023 weeknotes, though the page does not mention this earlier version alongside 0.64.6.
- Datasette 0.64.1 was released on 2023-01-11. The Datasette tutorial series' latest entry as of January 2023 is a SpatiaLite tutorial that builds a geospatial API mapping locations to time zones.
- datasette-faiss 0.1a0 (2023-01-11) maintains a FAISS index for specified Datasette tables, and datasette-openai 0.2 (2023-01-14) saves OpenAI API results to a SQLite database.
## New Information (2023-10-22-weeknotes)

- Cameron Yick contributed a JavaScript plugin API that lets plugins modify the Datasette interface, adding custom panels displayed above the main table view (shown as tabs when several plugins use the area) and extra options in the column cog action menu. (This describes a defining extensibility trait of Datasette's plugin system that is absent from the page.)

## New Information (2023-02-09-weeknotes)

- The Datasette table view refactor, JSON redesign and ?_extra= feature continued in February 2023, mainly in an ongoing pull request (simonw/datasette#1999) and a tracking issue (simonw/datasette#262). (The February 2023 weeknotes add the table view refactor and the ongoing development status of the JSON redesign and ?_extra= work, which the page does not record.)
- datasette-explain 0.1a0, an alpha Datasette plugin, adds a feature to the SQL query editing page that runs EXPLAIN QUERY PLAN on the query as the user types, shows any error message, and lists the tables and columns referenced by the query. (This plugin extends Datasette's query editing page, a Datasette feature not covered on the page.)
- Simon Willison is considering bringing live error checking, as shown by datasette-explain, into Datasette core, and notes that Datasette already has a mechanism for cutting off slow queries, which could make live query previews practical for queries that run in under about 100ms. (This describes a planned change to Datasette core and an existing query time-limit mechanism that the page does not mention.)

## Mentions in Source

- "**[datasette 0.64.6](https://github.com/simonw/datasette/releases/tag/0.64.6)**—2023-12-22  
  An open source multi-tool for exploring and publishing data" — [[_Inbox/2023-12-31-weeknotes|2023-12-31-weeknotes]]
- "**[datasette-haversine 0.2.1](https://github.com/simonw/datasette-haversine/releases/tag/0.2.1)**—2023-12-29  
  Datasette plugin that adds a custom SQL function for haversine distances" — [[_Inbox/2023-12-31-weeknotes|2023-12-31-weeknotes]]