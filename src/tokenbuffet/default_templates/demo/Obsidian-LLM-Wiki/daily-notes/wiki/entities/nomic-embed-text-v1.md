---
type: entity
created: 2026-10-21
updated: 2026-10-21
tags: [other]
aliases:
  - "nomic-embed-text"
  - "Nomic Embed Text v1"
sources:
  - "[[sources/2024-02-09-weeknotes_1bab97]]"
generation_complete: true
---

# nomic-embed-text-v1

## Description

nomic-embed-text-v1 is an embedding model that was newly released around the time of the February 2024 weeknotes. Support for it in the [[llm-sentence-transformers]] plugin required the new `--trust-remote-code` option. It is therefore an example of a concrete embedding model that the [[LLM]] tooling made usable through a plugin. The model was one of several [[Embeddings|embedding models]] the author worked with during this period.

## Related Entities

- [[entities/llm-sentence-transformers|llm-sentence-transformers]]
- [[entities/llm|LLM]]

## Related Concepts

- [[concepts/embedding-vector|Embeddings]]

## Mentions in Source

- "llm-sentence-transformers now has a `llm sentence-transformers register --trust-remote-code` option, which was necessary to support the newly released nomic-embed-text-v1 embedding model." — [[_Inbox/2024-02-09-weeknotes|2024-02-09-weeknotes]]