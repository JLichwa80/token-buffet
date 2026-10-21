---
type: entity
created: 2026-10-21
updated: 2026-10-21
tags: [project]
aliases:
  - "datasette-llm-embed plugin"
sources:
  - "[[sources/2023-09-17-weeknotes-embeddings_c2332f]]"

generation_complete: true
---

# datasette-llm-embed

## Description

datasette-llm-embed is a small [[Datasette]] plugin, released as version 0.1a0 on 2023-09-08, that adds an `llm_embed` SQL function. The function takes a model ID and a text string and returns an embedding, so embeddings can be generated directly inside SQL queries. Simon Willison built it to support quickly prototyping embedding-related ideas in Datasette. It connects the [[LLM]] embedding work to the Datasette ecosystem, and it is one of several plugins that extend [[LLM]] for [[Embeddings]] workflows.

## Related Entities

- [[entities/datasette|Datasette]]
- [[entities/llm|LLM]]

## Related Concepts

- [[concepts/embeddings|Embeddings]]

## Mentions in Source

- "One last embedding related project: `datasette-llm-embed` is a tiny plugin that adds a `select llm_embed('sentence-transformers/all-mpnet-base-v2', 'This is some text')` SQL function." — [[_Inbox/2023-09-17-weeknotes-embeddings|2023-09-17-weeknotes-embeddings]]