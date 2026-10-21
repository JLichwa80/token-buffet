---
type: concept
created: 2026-10-20
updated: 2026-10-21
generation_complete: true
sources:
  - "[[sources/2024-07-02-weeknotes_55c009]]"
  - "[[sources/2023-09-17-weeknotes-embeddings_c2332f]]"
tags:
  - "terminology"
aliases:
  - "FTS"
  - "BM25 full-text search"
---

# full-text search

## Definition

Full-text search is a retrieval method that indexes the words in documents so that they can be queried by keyword. In the source post, it is implemented as a BM25 full-text search index built with SQLite FTS and serves as the retrieval step in a [[RAG]] demonstration.

## Key Characteristics

- Indexes the words of each document, so queries match on keywords rather than on meaning.
- The source specifies BM25 ranking, implemented in SQLite FTS.
- Requires no embedding model: documents are not run through a model to produce vectors.
- Requires no vector index: the search is run against a keyword index rather than a [[vector search]] index.
- Simon Willison argues it is much easier to add to an existing site than embedding-based search.
- FTS entries are linked to their source row by rowid, so changing a table's rowid values breaks full-text search. Simon Willison found that `table.transform()` in sqlite-utils rewrote the rowid column on Datasette Cloud, and searches stopped returning correct results.
## Applications

- Retrieval step in search-based [[RAG]]: keywords are extracted from the user's question, searched against a full-text index, and the results are used to construct an answer. The source describes this pattern in its RAG demonstration built with [[Steve Krouse]] and [[Datasette]].
- Adding search to an existing website or database, such as a blog archive, where thousands of documents already exist and the cost of embedding them would be significant.
- Editing a table's schema with sqlite-utils after configuring full-text search on a column broke search results on Datasette Cloud, showing how easily a live site's search can fail after a schema change.
## Related Concepts

- [[concepts/rag|RAG]]

## Related Entities

- [[entities/simon-willison|Simon Willison]]
- [[entities/steve-krouse|Steve Krouse]]
- [[entities/datasette|Datasette]]

## Mentions in Source

- "It’s often much easier to bake FTS on to an existing site than embedding search, since it avoids the need to run embedding models against thousands of documents and then create a vector search index to run the queries against." — [[_Inbox/2024-07-02-weeknotes|2024-07-02-weeknotes]]
- "search for them using a BM25 full-text search index (in this case SQLite FTS) and construct an answer using the search results." — [[_Inbox/2024-07-02-weeknotes|2024-07-02-weeknotes]]
- "I spotted a bug on Datasette Cloud when I configured full-text search on a column, then edited the schema and found that searches no longer returned the correct results." — [[_Inbox/2023-09-17-weeknotes-embeddings|2023-09-17-weeknotes-embeddings]]