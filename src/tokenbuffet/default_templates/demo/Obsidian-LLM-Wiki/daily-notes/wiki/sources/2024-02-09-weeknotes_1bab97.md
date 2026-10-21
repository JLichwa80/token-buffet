---
type: source
created: 2026-10-21
updated: 2026-10-21
tags: [other]
aliases:
  - "Weeknotes: a Datasette release"
  - "an LLM release and a bunch of new plugins"
  - "2024-02-09-weeknotes"
contentHash: 2591-0bb201c3
source_file: "[[_Inbox/2024-02-09-weeknotes.md]]"
generation_complete: true
---

# 2024-02-09-weeknotes - Summary

## Source

- Original file: [[_Inbox/2024-02-09-weeknotes.md]]
- Ingested: 2026-10-21

## Core Content

This 9 February 2024 weeknotes post by Simon Willison covers the three weeks after his release notes for [[entities/datasette|Datasette]] 1.0a8 and [[entities/llm|LLM]] 0.13. It describes a wave of small, interconnected releases. [[entities/datasette-proxy-url|datasette-proxy-url]] was built to work around [[entities/substack|Substack]] blocking RSS requests from GitHub Actions, which the author solved by deploying a proxy on an existing Datasette instance, an example of [[concepts/datasette-as-a-cheap-deployment-platform|Datasette as a cheap deployment platform]]. Other new Datasette plugins include [[entities/datasette-homepage-table|datasette-homepage-table]], [[entities/datasette-events-db|datasette-events-db]] and [[entities/datasette-enrichments-quickjs|datasette-enrichments-quickjs]], which runs JavaScript against table rows through the QuickJS engine. [[entities/datasette-upload-csvs|datasette-upload-csvs]] gained per-database uploads. For LLM, the post covers [[entities/llm-embed-onnx|llm-embed-onnx]], [[entities/llm-gpt4all|llm-gpt4all]] and [[entities/llm-sentence-transformers|llm-sentence-transformers]], plus work on an in-progress [[concepts/rag|Retrieval Augmented Generation]] plugin. [[entities/shot-scraper|shot-scraper]] 1.4 added [[concepts/http-basic-authentication|HTTP Basic authentication]], and a revived [[entities/pge-outages|PG&E outage scraper]] began recording outages during storms.

## Key Entities

- [[entities/datasette|Datasette]] — the central platform for most plugins in the post
- [[entities/llm|LLM]] — the command-line tool and Python library that the LLM plugins extend
- [[entities/shot-scraper|shot-scraper]] — screenshot and scraping CLI built on Playwright, released as 1.4
- [[entities/datasette-enrichments|Datasette Enrichments]] — the enrichment feature that hosts row-transformation plugins
- [[entities/datasette-enrichments-quickjs|datasette-enrichments-quickjs]] — runs custom JavaScript against table rows via QuickJS
- [[entities/datasette-events-db|datasette-events-db]] — logs Datasette 1.0a8 events to a table
- [[entities/datasette-proxy-url|datasette-proxy-url]] — serves content proxied from another URL
- [[entities/datasette-homepage-table|datasette-homepage-table]] — shows a chosen table as a Datasette homepage
- [[entities/datasette-upload-csvs|datasette-upload-csvs]] — uploads CSVs into a specified database
- [[entities/llm-embed-onnx|llm-embed-onnx]] — makes ONNX embedding models available to LLM
- [[entities/llm-gpt4all|llm-gpt4all]] — adds GPT4All model support to LLM
- [[entities/llm-sentence-transformers|llm-sentence-transformers]] — embeddings via the sentence-transformers library
- [[entities/nomic-embed-text-v1|nomic-embed-text-v1]] — embedding model that required a trust-remote-code option
- [[entities/onnx-runtime|ONNX Runtime]] — inference engine underneath the ONNX embedding models
- [[entities/pge-outages|pge-outages]] — PG&E outage scraper revived for the February 2024 storms
- [[entities/substack|Substack]] — newsletter platform that blocked RSS requests from GitHub Actions

## Key Concepts

- [[concepts/rag|Retrieval Augmented Generation]] — the technique behind the in-progress llm-rag plugin
- [[concepts/embedding-vector|Embeddings]] — vector text representations that several LLM plugins add
- [[concepts/http-basic-authentication|HTTP Basic authentication]] — username and password support added to shot-scraper
- [[concepts/datasette-as-a-cheap-deployment-platform|Datasette as a cheap deployment platform]] — using an existing Datasette instance to host small services

## Main Points

- Datasette 1.0a8 and LLM 0.13 were covered in separate, earlier release notes; this post covers the three weeks after them.
- Several new Datasette plugins were released, including [[entities/datasette-proxy-url|datasette-proxy-url]], [[entities/datasette-homepage-table|datasette-homepage-table]], [[entities/datasette-events-db|datasette-events-db]] and [[entities/datasette-enrichments-quickjs|datasette-enrichments-quickjs]].
- The author worked around [[entities/substack|Substack]] blocking RSS requests from GitHub Actions by proxying the feed through a Datasette instance.
- LLM gained plugins for ONNX-based embedding models and GPT4All models, and a [[concepts/rag|Retrieval Augmented Generation]] plugin is in progress.
- [[entities/shot-scraper|shot-scraper]] 1.4 added [[concepts/http-basic-authentication|HTTP Basic authentication]] and bundled pull requests that had been waiting to be merged.
- [[entities/datasette-enrichments-quickjs|datasette-enrichments-quickjs]] runs on QuickJS, which appears to offer a sandbox with memory and time limits, a possibility the author finds exciting for Datasette.

## Mentions in Source

- "I solved it by deploying a quick proxy to a Datasette instance I already had up and running, effectively treating Datasette as a cheap deployment platform for random pieces of proxying infrastructure." — [[_Inbox/2024-02-09-weeknotes|2024-02-09-weeknotes]]
- "I released this partly as a debugging tool and partly because I like to ensure every Datasette plugin hook has at least one released plugin that uses it." — [[_Inbox/2024-02-09-weeknotes|2024-02-09-weeknotes]]
- "Plus it’s now tested against the Datasette 1.0 alpha series in addition to 0.x stable." — [[_Inbox/2024-02-09-weeknotes|2024-02-09-weeknotes]]
- "[LLM](https://llm.datasette.io/) is my command-line tool and Python library for interacting with Large Language Models." — [[_Inbox/2024-02-09-weeknotes|2024-02-09-weeknotes]]
- "I released updates for two LLM plugins as well:" — [[_Inbox/2024-02-09-weeknotes|2024-02-09-weeknotes]]
- "I finally started hacking on a `llm-rag` plugin which will provide an implementation of Retrieval Augmented Generation for LLM, similar to the process I describe in [Embedding paragraphs from my blog with E5-large-v2](https://til.simonwillison.net/llms/embed-paragraphs)." — [[_Inbox/2024-02-09-weeknotes|2024-02-09-weeknotes]]
- "[shot-scraper](https://shot-scraper.datasette.io/) is my CLI tool for taking screenshots of web pages and running scraping code against them using JavaScript, built on top of [Playwright](https://playwright.dev/)." — [[_Inbox/2024-02-09-weeknotes|2024-02-09-weeknotes]]
- "I dropped into the repo to add HTTP Basic authentication support and found several excellent PRs waiting to be merged, so I bundled those together into a new release." — [[_Inbox/2024-02-09-weeknotes|2024-02-09-weeknotes]]
- "New `--auth-username x --auth-password y` options for each `shot-scraper` command, allowing a username and password to be set for HTTP Basic authentication." — [[_Inbox/2024-02-09-weeknotes|2024-02-09-weeknotes]]