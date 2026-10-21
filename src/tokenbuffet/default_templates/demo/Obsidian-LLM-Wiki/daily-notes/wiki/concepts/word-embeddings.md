---
type: concept
created: 2026-10-21
updated: 2026-10-21
generation_complete: true
sources:
  - "[[sources/2023-10-22-weeknotes_1435b6]]"
  - "[[sources/2023-09-17-weeknotes-embeddings_c2332f]]"
  - "[[sources/2023-01-15-weeknotes_aefc7f]]"
tags:
  - "terminology"
aliases:
  - "Embeddings"
  - "Word vectors"
---

# Word embeddings

## Definition

Word embeddings are dense, real-valued vector representations of words, learned so that words with similar meanings or usage sit close together in the vector space. Simon Willison's PyBay 2023 talk, "Embeddings: What they are and why they matter," explains the concept and its significance.

## Key Characteristics

- Each word is mapped to a fixed-length vector of numbers rather than a discrete symbol.
- Geometric distance between vectors (for example, cosine similarity) reflects semantic or distributional similarity.
- Vectors are learned from large text corpora, so they encode patterns of word usage.
- Embeddings are a foundational representation for downstream tasks such as search, clustering, and classification.
- The topic is a recurring interest for its author, as shown by the linked posts tagged with embeddings.

## Applications

- Semantic search and retrieval, where queries and documents are compared by vector similarity.
- Clustering and grouping of text by meaning.
- Feature input for classification and recommendation models.
- Extension beyond text to other media, such as deploying an image-text embedding model, which the author covered in a related TIL.

## Related Concepts

- [[concepts/datasette-metadata|Datasette metadata]]

## Related Entities

- [[entities/pybay-2023|PyBay 2023]]

## Mentions in Source

- "I gave a talk [at PyBay 2023](https://pybay.com/) called “Embeddings: What they are and why they matter”, digging into the weird and fun world of word embeddings (see [previous posts](https://simonwillison.net/tags/embeddings/))." — [[_Inbox/2023-10-22-weeknotes|2023-10-22-weeknotes]]
- "I’ll be posting detailed notes from that talk tomorrow." — [[_Inbox/2023-10-22-weeknotes|2023-10-22-weeknotes]]