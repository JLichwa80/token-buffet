---
type: entity
created: 2026-10-21
updated: 2026-10-21
generation_complete: true
tags: [project]
aliases:
  - "llm-cluster plugin"
sources:
  - "[[sources/2023-09-17-weeknotes-embeddings_c2332f]]"

---

# llm-cluster

## Description

llm-cluster is an [[LLM]] plugin, released as version 0.2 on 2023-09-04, that clusters [[Embeddings]] to find groups of related items. Its most distinctive feature is that it can send the items in each cluster through another language model to generate a short name for the cluster. The source gives an example command, `llm cluster issues 10 -d issues.db --summary --prompt 'Short, concise title for this cluster of related documents'`, which clusters issues from a database and produces a title for each cluster. Simon Willison describes this as a practical application of the embedding work covered in the September 2023 weeknotes. It extends LLM's embedding support into [[Semantic search]]-style grouping of content.

## Related Entities

- [[entities/llm|LLM]]

## Related Concepts

- [[concepts/embeddings|Embeddings]]
- [[concepts/semantic-search|Semantic search]]

## Mentions in Source

- "The neatest feature of `llm-cluster` is that you can ask it to generate names for these clusters by sending the names of the items in each cluster through another language model, something like this:" — [[_Inbox/2023-09-17-weeknotes-embeddings|2023-09-17-weeknotes-embeddings]]