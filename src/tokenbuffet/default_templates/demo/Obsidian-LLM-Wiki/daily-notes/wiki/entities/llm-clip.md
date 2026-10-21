---
type: entity
created: 2026-10-21
updated: 2026-10-21
tags: [project]
aliases:
  - "llm-clip plugin"
sources:
  - "[[sources/2023-09-17-weeknotes-embeddings_c2332f]]"

generation_complete: true
---

# llm-clip

## Description

llm-clip is an [[LLM]] plugin released in version 0.1 that generates embeddings for images and text using [[CLIP]]. Simon Willison released it in September 2023 as one of two embedding plugins, alongside [[llm-sentence-transformers]]. The source calls it the most fun of the two because it enables a local image search engine. It shows how the LLM plugin system extends embedding support to new model types. Its embeddings are an instance of the [[Embeddings]] concept.

## Related Entities

- [[entities/llm|LLM]]
- [[entities/clip|CLIP]]

## Related Concepts

- [[concepts/embeddings|Embeddings]]

## Mentions in Source

- "The CLIP one is particularly fun, because it genuinely allows you to build a sophisticated image search engine that runs entirely on your own computer!" — [[_Inbox/2023-09-17-weeknotes-embeddings|2023-09-17-weeknotes-embeddings]]