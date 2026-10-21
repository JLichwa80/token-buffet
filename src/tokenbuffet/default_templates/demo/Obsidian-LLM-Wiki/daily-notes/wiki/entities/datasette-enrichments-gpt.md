---
type: entity
created: 2026-10-20
updated: 2026-10-20
generation_complete: true
sources:
  - "[[sources/2024-05-28-weeknotes_18b318]]"
  - "[[sources/2024-04-10-weeknotes-llm-releases_18e6bc]]"
  - "[[sources/2024-03-16-weeknotes-the-aftermath-of-nicar_29f231]]"
tags:
  - "project"
  - "other"
---

# datasette-enrichments-gpt

> Stub created by the ingest candidate gate (prose+named). 2024-05-28-weeknotes_18b318 names this without treating it. Will be filled by the next ingest of a source that does.

datasette-enrichments-gpt is a Datasette plugin that provides enrichment for analyzing row data with OpenAI's GPT models. It can enrich data in a table by running prompts through GPT-3.5, GPT-4 Turbo or GPT-4 Vision. The author released version 0.5 in May 2024, adding support for GPT-4o. It is one of several tools the author released alongside datasette-extract and llm to support the new models. The plugin sits within the wider Datasette ecosystem that the author maintains.

In March 2024, the author demonstrated datasette-enrichments-gpt, described as a GPT-4 powered Datasette plugin, in a lightning talk at NICAR 2024. The demo also covered datasette-extract, which the author said they needed to write more about.

> "I released [LLM 0.14](https://github.com/simonw/llm/releases/tag/0.14), [datasette-extract 0.1a7](https://github.com/datasette/datasette-extract/releases/tag/0.1a7) and [datasette-enrichments-gpt 0.5](https://github.com/datasette/datasette-enrichments-gpt/releases/tag/0.5) with support for GPT-4o, and [llm-gemini 0.1a4](https://github.com/simonw/llm-gemini/releases/tag/0.1a4) adding support for the new inexpensive Gemini 1.5 Flash." — 2024-05-28-weeknotes_18b318

## Related Entities

- [[entities/google-gemini-pro-1-5|Google Gemini Pro 1.5]]
- [[entities/gpt-4-turbo|GPT-4 Turbo]]
- [[entities/mixtral-8x22b|Mixtral 8x22B]]
- [[entities/datasette-extract|datasette-extract]]
- [[entities/datasette|Datasette]]
- [[entities/nicar|NICAR]]
- [[entities/gpt-4|GPT-4]]

## Related Concepts

- [[concepts/plugin-hook|plugin hook]]

## New Information (2024-04-10-weeknotes-llm-releases)

- The datasette-enrichments-gpt plugin can enrich data in a table by running prompts through GPT-3.5, GPT-4 Turbo or GPT-4 Vision. (This adds the specific model families the plugin supports, which the existing Description only describes generically as OpenAI's GPT models.)
- Version 0.4 of datasette-enrichments-gpt (released 2024-04-10) switched the plugin to the new GPT-4 Turbo model. (This is a dated release fact about the plugin's version history that the existing page does not record.)

## New Information (2024-03-16-weeknotes-the-aftermath-of-nicar)

- Simon Willison demonstrated datasette-enrichments-gpt, described as a GPT-4 powered Datasette plugin, in a lightning talk at NICAR 2024, alongside datasette-extract. (This is a new dated fact about the plugin's public demonstration that fits the existing Description section.)

## Mentions in Source

- "I gave a lightning talk demonstrating two new GPT-4 powered Datasette plugins—datasette-enrichments-gpt and datasette-extract." — [[_Inbox/2024-03-16-weeknotes-the-aftermath-of-nicar|2024-03-16-weeknotes-the-aftermath-of-nicar]]
- "Another small release: the [datasette-enrichments-gpt](https://datasette.io/plugins/datasette-enrichments-gpt) plugin can enrich data in a table by running prompts through GPT-3.5, GPT-4 Turbo or GPT-4 Vision." — [[_Inbox/2024-04-10-weeknotes-llm-releases|2024-04-10-weeknotes-llm-releases]]
- "I released [version 0.4](https://github.com/datasette/datasette-enrichments-gpt/releases/tag/0.4) switching to the new GPT-4 Turbo model." — [[_Inbox/2024-04-10-weeknotes-llm-releases|2024-04-10-weeknotes-llm-releases]]