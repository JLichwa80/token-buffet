---
type: concept
created: 2026-10-20
updated: 2026-10-21
generation_complete: true
sources:
  - "[[sources/2024-07-02-weeknotes_55c009]]"
  - "[[sources/2023-01-15-weeknotes_aefc7f]]"
tags:
  - "terminology"
aliases:
  - "embedding search"
  - "embeddings-based RAG"
  - "Vector similarity search"
---

# vector search

## Definition

Vector search is a retrieval approach that represents text as embeddings and finds relevant documents by comparing vectors in an index. Documents are matched by vector similarity rather than by keyword overlap.

## Key Characteristics

- Represents text as embedding vectors produced by embedding models.
- Retrieves documents by comparing query vectors against vectors in an index.
- Requires running an embedding model across the full document set and building a vector index before any query can run.
- Is harder to reason about than keyword-based retrieval, according to [[Simon Willison]].
- Is considerably more expensive to adopt than [[full-text search]] when adding search to an existing site, according to [[Simon Willison]].

## Applications

- Serving as the retrieval step in [[RAG]] pipelines that rely on embeddings.
- Adding semantic search to a site or corpus where embedding and indexing costs are acceptable.
- In the 2024-07-02 weeknotes, serving as the alternative against which the simpler FTS-based [[RAG]] pattern is favoured.
- Implemented with FAISS, a fast vector similarity search library, packaged as the datasette-faiss plugin that builds a FAISS index for specified Datasette tables.
- Serves as the retrieval step of a documentation Q&A system, locating the passages most relevant to a user's question and connecting embeddings to answer generation.
## Related Concepts

- [[concepts/rag|RAG]]
- [[concepts/full-text-search|full-text search]]
- [[concepts/embeddings|embeddings]]

## Related Entities

- [[entities/simon-willison|Simon Willison]]

## Mentions in Source

- "It’s considerably easier to reason about than RAG using vector search based on embeddings, and can provide high quality results with a relatively simple implementation." — [[_Inbox/2024-07-02-weeknotes|2024-07-02-weeknotes]]
- "a plugin that builds a FAISS index for fast vector similarity search" — [[_Inbox/2023-01-15-weeknotes|2023-01-15-weeknotes]]
- "Maintain a FAISS index for specified Datasette tables" — [[_Inbox/2023-01-15-weeknotes|2023-01-15-weeknotes]]