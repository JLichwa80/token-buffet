---
type: concept
created: 2026-10-21
updated: 2026-10-21
tags: [idea]
aliases:
  - "Vector search"
  - "Embedding-based search"
sources:
  - "[[sources/2023-09-17-weeknotes-embeddings_c2332f]]"

generation_complete: true
---

# Semantic search

## Definition

Semantic search finds content by its meaning rather than by exact keyword matches. It is typically built on [[Embeddings]], which represent text as vectors so that items with similar meaning end up close together.

## Key Characteristics

- Matches on meaning, so a query can find relevant content that uses different wording from the query.
- Relies on [[Embeddings]] to convert content and queries into comparable vectors.
- Can be applied to unusual content types, such as source code, where the query describes what a function does rather than naming it.
- Works as a retrieval step that other systems can build on, such as [[RAG]] pipelines.

## Applications

- **Code discovery:** finding a function by describing its behavior, such as a function that downloads a CSV. Willison describes embedding support as making this kind of semantic function search easy to build.
- **Blog and content search:** Willison built a command-line semantic search engine for his blog using paragraph embeddings.
- **Tooling workflows:** the `symbex` and `llm embed-multi` workflow, driven by the [[LLM]] CLI, connects embedding generation to practical code discovery.

## Related Concepts

- [[concepts/embeddings|Embeddings]]
- [[concepts/rag|rag]]

## Related Entities

- [[entities/llm|LLM]]

## Mentions in Source

- "I haven’t fully explored what this enables yet, but it should mean that both related functions and semantic function search (“Find my a function that downloads a CSV”) are now easy to build." — [[_Inbox/2023-09-17-weeknotes-embeddings|2023-09-17-weeknotes-embeddings]]