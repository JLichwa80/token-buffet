---
type: concept
created: 2026-10-20
updated: 2026-10-20
generation_complete: true
sources:
  - "[[sources/2024-05-28-weeknotes_18b318]]"
  - "[[sources/2024-04-10-weeknotes-llm-releases_18e6bc]]"
tags:
  - "idea"
aliases:
  - "structured extraction"
---

# Structured data extraction

## Definition

Structured data extraction is the process of turning unstructured input, such as text or images, into structured rows and tables using a [[Large Language Models|language model]].

## Key Characteristics

- Converts unstructured input (text, images) into structured rows and tables.
- Relies on a language model to perform the extraction.
- Output is tabular, so it can be stored, queried, and reviewed like any dataset.
- Reliability depends on the model. The source reports that [[GPT-4o]] is more reliable than earlier options at producing long sequences of extracted rows.

## Applications

- Pulling tabular data out of text passages and images. The source author does this with [[datasette-extract]].
- Loading extracted rows into [[Datasette]] tables for browsing and querying, which links this concept to the author's Datasette tooling.
- Evaluating which models can produce long, consistent row sequences without dropping or corrupting entries.
- [[datasette-extract]] is a plugin for [[Datasette]] that adds structured data extraction from unstructured text, powered by GPT-4 Turbo.
## Related Concepts

- [[concepts/large-language-models|Large Language Models]]

## Related Entities

- [[entities/datasette-extract|datasette-extract]]
- [[entities/gpt-4o|GPT-4o]]
- [[entities/datasette|Datasette]]

## Mentions in Source

- "I’ve been getting particularly good results from it for structured data extraction" — [[_Inbox/2024-05-28-weeknotes|2024-05-28-weeknotes]]
- "it seems to be able to more reliably produce a longer sequence of extracted rows from a given input." — [[_Inbox/2024-05-28-weeknotes|2024-05-28-weeknotes]]
- "I’ve been working on [Datasette Extract](https://datasette.io/plugins/datasette-extract) for a while now: it’s a plugin for Datasette that adds structured data extraction from unstructured text, powered by GPT-4 Turbo." — [[_Inbox/2024-04-10-weeknotes-llm-releases|2024-04-10-weeknotes-llm-releases]]