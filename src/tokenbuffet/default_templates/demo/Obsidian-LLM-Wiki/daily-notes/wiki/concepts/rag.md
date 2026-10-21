---
type: concept
created: 2026-10-20
updated: 2026-10-21
generation_complete: true
sources:
  - "[[sources/2024-07-02-weeknotes_55c009]]"
  - "[[sources/2024-02-27-weeknotes-getting-ready-for-nicar_823782]]"
  - "[[sources/2024-02-09-weeknotes_1bab97]]"
  - "[[sources/2023-09-17-weeknotes-embeddings_c2332f]]"
tags:
  - "terminology"
aliases:
  - "Retrieval-Augmented Generation"
  - "RAG pattern"
  - "Retrieval Augmented Generation"
---

# RAG

## Definition

RAG (Retrieval-Augmented Generation) is a technique in which a user's question is turned into search keywords, those keywords are used to query an index, and an answer is generated from the retrieved results. In the weeknotes post, [[Simon Willison]] and [[Steve Krouse]] build a RAG system over Simon's blog on [[Val Town]], using SQLite full-text search ([[full-text search]]) as the retrieval backend.

## Key Characteristics

- Retrieval step: the question is converted into keywords rather than an embedding.
- Search backend: a full-text index (SQLite FTS in the post).
- Generation step: the answer is composed from the search results, with [[Claude 3.5 Sonnet]] as the model used in the post.
- Preferred over embedding-based vector RAG by its advocate because it is easier to reason about and can perform well with a simpler implementation.
- Low cost to add to an existing site, since it reuses a search index rather than requiring an embedding pipeline.
- Alternative retrieval variant: an earlier, planned llm-rag approach embeds blog paragraphs with E5-large-v2, so retrieval is embedding-based rather than keyword search.
## Applications

- Question answering over a site or blog that already has content, such as Simon Willison's blog built on Val Town.
- Adding AI-assisted search to an existing website without introducing vector databases or embedding infrastructure.
- Lightweight code Q&A without an index: use ripgrep's context options (`-B`/`-A` lines around each match) to gather just enough surrounding lines, then pipe them into `llm` to answer questions about the code.
- Simon Willison started building an [llm-rag](https://github.com/simonw/llm-rag) plugin for the LLM CLI tool, providing a Retrieval Augmented Generation implementation (February 2024).
## Related Concepts

- [[concepts/full-text-search|full-text search]]

## Related Entities

- [[entities/simon-willison|Simon Willison]]
- [[entities/steve-krouse|Steve Krouse]]
- [[entities/val-town|Val Town]]
- [[entities/claude-3-5-sonnet|Claude 3.5 Sonnet]]

## Mentions in Source

- "I guess this is another super lightweight form of RAG: you can use the rg context options (include X lines before/after each match) to assemble just enough context to get useful answers to questions about code." — [[_Inbox/2024-02-27-weeknotes-getting-ready-for-nicar|2024-02-27-weeknotes-getting-ready-for-nicar]]
- "We built an implementation of RAG against my blog, demonstrating the RAG technique where you extract keywords from the user’s question, search for them using a BM25 full-text search index (in this case SQLite FTS) and construct an answer using the search results." — [[_Inbox/2024-07-02-weeknotes|2024-07-02-weeknotes]]
- "The more time I spend with this RAG pattern the more I like it." — [[_Inbox/2024-07-02-weeknotes|2024-07-02-weeknotes]]
- "I finally started hacking on a `llm-rag` plugin which will provide an implementation of Retrieval Augmented Generation for LLM, similar to the process I describe in [Embedding paragraphs from my blog with E5-large-v2](https://til.simonwillison.net/llms/embed-paragraphs)." — [[_Inbox/2024-02-09-weeknotes|2024-02-09-weeknotes]]
- "I’ll write more about that once it’s in an interesting state." — [[_Inbox/2024-02-09-weeknotes|2024-02-09-weeknotes]]