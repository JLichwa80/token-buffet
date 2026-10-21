---
type: entity
created: 2026-10-21
updated: 2026-10-21
generation_complete: true
sources:
  - "[[sources/2024-02-09-weeknotes_1bab97]]"
  - "[[sources/2023-09-17-weeknotes-embeddings_c2332f]]"
tags:
  - "project"
aliases:
  - "llm-sentence-transformers 0.2"
---

# llm-sentence-transformers

## Description

llm-sentence-transformers is an LLM plugin that provides embeddings through the sentence-transformers library, extending the [[entities/llm|LLM]] command-line tool with additional embedding models. Version 0.2 was released on 2024-02-04. The release added a `llm sentence-transformers register --trust-remote-code` option, which was needed to support the newly released [[entities/nomic-embed-text-v1|nomic-embed-text-v1]] embedding model. The plugin is one of the LLM plugin updates covered in the weeknotes, and it provides [[concepts/embedding-vector|Embeddings]] support within LLM.

## Related Entities

- [[entities/llm|LLM]]
- [[entities/nomic-embed-text-v1|nomic-embed-text-v1]]

## Related Concepts

- [[concepts/embedding-vector|Embeddings]]

## Mentions in Source

- "llm-sentence-transformers now has a `llm sentence-transformers register --trust-remote-code` option, which was necessary to support the newly released nomic-embed-text-v1 embedding model." — [[_Inbox/2024-02-09-weeknotes|2024-02-09-weeknotes]]