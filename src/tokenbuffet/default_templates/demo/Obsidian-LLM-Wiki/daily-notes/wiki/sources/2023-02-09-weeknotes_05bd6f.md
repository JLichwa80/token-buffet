---
type: source
created: 2026-10-21
updated: 2026-10-21
tags: [other]
aliases:
  - "Weeknotes: A bunch of things I learned this week"
  - "plus datasette-explain"
  - "2023-02-09-weeknotes"
contentHash: 2d88-574ea6da
source_file: "[[_Inbox/2023-02-09-weeknotes.md]]"
generation_complete: true
---

# 2023-02-09-weeknotes - Summary

## Source

- Original file: [[_Inbox/2023-02-09-weeknotes.md]]
- Ingested: 2026-10-21

## Core Content

This 9 February 2023 weeknotes post by Simon Willison covers the week's work on [[entities/datasette|Datasette]], centered on a table view refactor, a JSON redesign, and the `?_extra=` feature. Much of the post is an annotated list of [[concepts/til|TILs]] (Today I Learned notes). Research highlights include running the [[entities/gtr-t5-large|gtr-t5-large]] embeddings model locally on a MacBook M2, and training a [[concepts/gpt-style-generative-language-model|GPT-style model]] from scratch with [[entities/nanogpt|nanoGPT]] on the author's blog, which produced output he called junk. Other TILs cover running untrusted Python in a sandbox with [[entities/wasmtime|wasmtime]] and [[concepts/python-in-webassembly|Python in WebAssembly]], a Mastodon bot built with [[entities/github-actions|GitHub Actions]] and [[entities/toot|toot]], [[concepts/recursive-ctes|recursive CTEs]], [[concepts/subqueries-in-select-expressions|subqueries in select expressions]], and [[entities/apache-bench|Apache Bench]] error messages. The main release is [[entities/datasette-explain|datasette-explain]] 0.1a0, which runs [[concepts/explain-query-plan|EXPLAIN QUERY PLAN]] as the user types. The author is most enthusiastic about its [[concepts/live-error-checking|live error checking]]. The post also notes releases of [[entities/db-to-sqlite|db-to-sqlite]] 1.5 and [[entities/shot-scraper|shot-scraper]] 1.1.1.

## Key Entities

- [[entities/datasette|Datasette]]: the open-source data exploration tool that is the main subject of the week's work.
- [[entities/datasette-explain|datasette-explain]]: the new 0.1a0 plugin highlighted in the post.
- [[entities/sqlite|SQLite]]: the database engine underneath Datasette and the subject of several TILs.
- [[entities/nanogpt|nanoGPT]]: Andrej Karpathy's GPT-style training project, used to train a small model.
- [[entities/gtr-t5-large|gtr-t5-large]]: a sentence embeddings model run locally on a MacBook M2.
- [[entities/wasmtime|wasmtime]]: the WebAssembly runtime used to sandbox untrusted Python.
- [[entities/datasette-lite|Datasette Lite]]: the browser-based Datasette build that uses Python in WebAssembly.
- [[entities/tim-bart|Tim Bart]]: the person who found the working wasmtime example.
- [[entities/mastodon|Mastodon]]: the platform the author moved his Covid sewage bot to.
- [[entities/toot|toot]]: the Python library and CLI for Mastodon used by the bot.
- [[entities/github-actions|GitHub Actions]]: used to schedule the Mastodon bot.
- [[entities/db-to-sqlite|db-to-sqlite]]: a CLI for exporting data from SQL databases to SQLite, released as 1.5.
- [[entities/shot-scraper|shot-scraper]]: a CLI for automated website screenshots, released as 1.1.1.
- [[entities/apache-bench|Apache Bench]]: the load-testing tool whose "length" errors are explained in a TIL.
- [[entities/openai-embeddings-api|OpenAI embeddings API]]: referenced as the embeddings approach the author described weeks earlier.
- [[entities/pypi|PyPI]]: the Python package index where the author checked name availability.

## Key Concepts

- [[concepts/explain-query-plan|EXPLAIN QUERY PLAN]]: the SQLite command that datasette-explain runs on each query.
- [[concepts/live-error-checking|Live error checking]]: validating SQL as it is typed; the feature the author most wants in Datasette core.
- [[concepts/recursive-ctes|Recursive CTEs]]: SQL common table expressions used to query hierarchical data.
- [[concepts/subqueries-in-select-expressions|Subqueries in select expressions]]: a pattern for fetching a row with a limited set of related rows in one query.
- [[concepts/gpt-style-generative-language-model|GPT-style generative language model]]: a text-generating model, contrasted with embeddings models.
- [[concepts/python-in-webassembly|Python in WebAssembly]]: Python builds that run inside a WebAssembly runtime.
- [[concepts/til|TIL]]: the author's "Today I Learned" note format.

## Main Points

- The week's main development work was on Datasette's table view refactor, JSON redesign, and `?_extra=` feature, tracked in an ongoing pull request.
- The author ran the gtr-t5-large embeddings model locally on a MacBook M2 and found it gave good results for finding similar content.
- The author trained a GPT-style model from scratch with nanoGPT on his blog text. The output was poor but still reflected his voice.
- Running untrusted Python in a WebAssembly sandbox became possible with wasmtime, using an example from Tim Bart and the VMware Python WASM build.
- The author moved a Covid sewage bot to Mastodon, using scheduled GitHub Actions and toot.
- datasette-explain 0.1a0 runs EXPLAIN QUERY PLAN on SQL as the user types, showing errors, the query plan, and related table columns. It is an alpha release.
- The author is most interested in datasette-explain's live error checking and is considering bringing it to Datasette core.
- Live result previews could work for queries that finish in under about 100ms, which Datasette's existing query cutoff mechanism supports.

## Mentions in Source

- "The Datasette table view refactor, JSON redesign and `?_extra=` continues this week, mainly in [this ongoing pull request](https://github.com/simonw/datasette/pull/1999) and [this tracking issue](https://github.com/simonw/datasette/issues/262)." — [[_Inbox/2023-02-09-weeknotes|2023-02-09-weeknotes]]
- "Datasette has a good mechanism for cutting off queries that take too long to load, so I could try previewing queries but only if they can be run in less than 100ms or so." — [[_Inbox/2023-02-09-weeknotes|2023-02-09-weeknotes]]
- "This is partly an experiment in what it feels like for Datasette to run interactive code relating to queries as you type them." — [[_Inbox/2023-02-09-weeknotes|2023-02-09-weeknotes]]
- "Just one new plugin this week: [datasette-explain](https://github.com/simonw/datasette-explain), which adds a feature to the Datasette SQL query editing page which constantly runs `explain query plan ...` on the query you’re typing and shows the results." — [[_Inbox/2023-02-09-weeknotes|2023-02-09-weeknotes]]
- "The plugin works by sending the SQL query you have typed to a `/db/-/explain` endpoint in the background." — [[_Inbox/2023-02-09-weeknotes|2023-02-09-weeknotes]]
- "This plugin is very much an alpha: I’m not convinced it’s displaying the right data in the right way yet." — [[_Inbox/2023-02-09-weeknotes|2023-02-09-weeknotes]]
- "... even more exciting, I *did* manage to train and run a GPT-style generative language model! I used [nanoGPT](https://github.com/karpathy/nanoGPT) by Andrej Karpathy, which trains really nicely on an M2." — [[_Inbox/2023-02-09-weeknotes|2023-02-09-weeknotes]]
- "This is trained from scratch, it’s not from a pre-existing language model." — [[_Inbox/2023-02-09-weeknotes|2023-02-09-weeknotes]]
- "I mean, it’s total junk... but it does have a hint of my voice to it." — [[_Inbox/2023-02-09-weeknotes|2023-02-09-weeknotes]]