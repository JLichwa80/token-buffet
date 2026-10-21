---
type: source
created: 2026-10-21
updated: 2026-10-21
tags: [other]
aliases:
  - "Weeknotes: Plugins for LLM"
  - "sqlite-utils and Datasette"
  - "2023-08-05-weeknotes-plugins"
contentHash: 273f-5a9e5357
source_file: "[[_Inbox/2023-08-05-weeknotes-plugins.md]]"
generation_complete: true
---

# 2023-08-05-weeknotes-plugins - Summary

## Source

- Original file: [[_Inbox/2023-08-05-weeknotes-plugins.md]]
- Ingested: 2026-10-21

## Core Content

Simon Willison's weeknotes of 5 August 2023 cover plugin work across three projects. In [[entities/llm|LLM]], support for models beyond OpenAI's was added through [[concepts/plugins|plugins]]. This made it possible to run [[entities/llama-2|Llama 2]] via the [[entities/replicate|Replicate]] plugin on its launch day, and locally through [[entities/llm-llama-cpp|llm-llama-cpp]], which uses [[entities/llama-cpp|llama.cpp]] and [[concepts/ggml|GGML]] quantization. [[entities/sqlite-utils|sqlite-utils]] gained a plugin system with two categories, CLI commands and [[concepts/custom-sql-functions|custom SQL functions]]. Its [[entities/sqlite-utils-shell|sqlite-utils-shell]] plugin was replaced by [[entities/sqlite-utils-litecli|sqlite-utils-litecli]], which wraps [[entities/litecli|litecli]]. In [[entities/datasette|Datasette]] work for [[entities/datasette-cloud|Datasette Cloud]], [[entities/datasette-auth-tokens|datasette-auth-tokens]] gained interactive creation and revocation of [[concepts/api-tokens|API tokens]]. The [[entities/dclient|dclient]] 0.2 release added an insert command for the [[concepts/write-api|write API]]. The post also covers a closing talk at [[entities/north-bay-python|North Bay Python]], [[entities/catching-up-on-the-weird-world-of-llms|Catching up on the weird world of LLMs]], and ends with lists of posts, releases and TIL entries.

## Key Entities

- [[entities/llm|LLM]]: command-line tool extended with model plugins
- [[entities/llm-llama-cpp|llm-llama-cpp]]: runs a GGML-quantized Llama 2 model locally
- [[entities/llama-2|Llama 2]]: first commercially usable version of Meta's LLaMA model
- [[entities/replicate|Replicate]]: model hosting platform used by the llm-replicate plugin
- [[entities/llama-cpp|llama.cpp]]: inference engine behind llm-llama-cpp
- [[entities/homebrew|Homebrew]]: package manager where LLM became available in core
- [[entities/sqlite-utils|sqlite-utils]]: CLI and Python library for SQLite, now with plugins
- [[entities/sqlite-utils-shell|sqlite-utils-shell]]: early shell plugin, later superseded
- [[entities/sqlite-utils-litecli|sqlite-utils-litecli]]: litecli shell exposing installed SQL functions
- [[entities/litecli|litecli]]: SQLite terminal shell with auto-completion
- [[entities/datasette|Datasette]]: ecosystem for working with small data
- [[entities/datasette-cloud|Datasette Cloud]]: SaaS hosted version of Datasette
- [[entities/datasette-auth-tokens|datasette-auth-tokens]]: token-based authentication plugin
- [[entities/dclient|dclient]]: CLI for interacting with Datasette instances via API
- [[entities/north-bay-python|North Bay Python]]: conference where the closing LLM talk was given
- [[entities/catching-up-on-the-weird-world-of-llms|Catching up on the weird world of LLMs]]: closing talk, published as an annotated presentation

## Key Concepts

- [[concepts/plugins|Plugins]]: extensions that add features without changing core code
- [[concepts/custom-sql-functions|Custom SQL functions]]: user-defined functions callable from SQLite
- [[concepts/large-language-models|Large Language Model]]: neural language model trained on large text corpora
- [[concepts/ggml|GGML]]: quantized model format enabling local inference
- [[concepts/write-api|Write API]]: Datasette 1.0 HTTP interface for writing data
- [[concepts/api-tokens|API tokens]]: credentials gating access to Datasette instances

## Main Points

- [[entities/llm|LLM]] gained support for non-OpenAI models, enabling [[entities/llama-2|Llama 2]] use within days of its release.
- [[entities/llm-llama-cpp|llm-llama-cpp]] runs a GGML-quantized [[entities/llama-2|Llama 2]] model directly on local hardware.
- [[entities/sqlite-utils|sqlite-utils]] added [[concepts/plugins|plugins]] in two categories: CLI commands and [[concepts/custom-sql-functions|custom SQL functions]].
- [[entities/sqlite-utils-litecli|sqlite-utils-litecli]] replaced the earlier [[entities/sqlite-utils-shell|sqlite-utils-shell]] as a full-featured shell.
- [[entities/datasette-auth-tokens|datasette-auth-tokens]] 0.4a0 lets [[concepts/api-tokens|API tokens]] be created and revoked interactively for [[entities/datasette-cloud|Datasette Cloud]] automatic imports.
- [[entities/dclient|dclient]] 0.2 inserts CSV, TSV or JSON data via the [[concepts/write-api|Datasette 1.0 write API]].
- A [[entities/north-bay-python|North Bay Python]] talk on LLMs was published as an annotated presentation with a full transcript.

## Mentions in Source

- "I added the ability to support models other than the OpenAI ones to my [LLM](https://llm.datasette.io/) command-line tool [last month](https://simonwillison.net/2023/Jul/12/llm/)." — [[_Inbox/2023-08-05-weeknotes-plugins|2023-08-05-weeknotes-plugins]]
- "LLM is [available in Homebrew core now](https://formulae.brew.sh/formula/llm), so getting Llama 2 working is as simple as:" — [[_Inbox/2023-08-05-weeknotes-plugins|2023-08-05-weeknotes-plugins]]
- "My [sqlite-utils](https://sqlite-utils.datasette.io/) project, similar to LLM, is a combined CLI tool and Python library." — [[_Inbox/2023-08-05-weeknotes-plugins|2023-08-05-weeknotes-plugins]]
- "Based on requests from the community I [adding plugin support to it](https://simonwillison.net/2023/Jul/24/sqlite-utils-plugins/) too." — [[_Inbox/2023-08-05-weeknotes-plugins|2023-08-05-weeknotes-plugins]]
- "Meanwhile, in Datasette land... I’ve been investing more time building [Datasette Cloud](https://www.datasette.cloud/), the SaaS cloud hosted version of Datasette." — [[_Inbox/2023-08-05-weeknotes-plugins|2023-08-05-weeknotes-plugins]]
- "The Datasette 1.0 alphas introduced a write API." — [[_Inbox/2023-08-05-weeknotes-plugins|2023-08-05-weeknotes-plugins]]
- "I wanted a mechanism for Datasette Cloud users to be able to setup automatic imports of data into their instances, taking advantage of that API." — [[_Inbox/2023-08-05-weeknotes-plugins|2023-08-05-weeknotes-plugins]]
- "I’ll have more news to share about Datasette Cloud soon!" — [[_Inbox/2023-08-05-weeknotes-plugins|2023-08-05-weeknotes-plugins]]
- "A few days ago I took that a step further: the new [llm-llama-cpp](https://github.com/simonw/llm-llama-cpp) plugin can now be used to run a GGML quantized version of the Llama 2 model directly on your own hardware." — [[_Inbox/2023-08-05-weeknotes-plugins|2023-08-05-weeknotes-plugins]]