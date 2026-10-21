---
type: concept
created: 2026-10-20
updated: 2026-10-21
generation_complete: true
sources:
  - "[[sources/2024-04-10-weeknotes-llm-releases_18e6bc]]"
  - "[[sources/2024-02-09-weeknotes_1bab97]]"
  - "[[sources/2023-10-30-weeknotes_d4a215]]"
  - "[[sources/2023-09-17-weeknotes-embeddings_c2332f]]"
  - "[[sources/2023-01-15-weeknotes_aefc7f]]"
tags:
  - "terminology"
aliases:
  - "Embeddings"
---

# embedding vector

> Stub created by the ingest candidate gate (prose+named) — [[sources/2024-04-10-weeknotes-llm-releases_18e6bc]] names this without treating it. Will be filled by the next ingest of a source that does.

An embedding vector is a numerical representation of text or other content, used to store and compare meaning. The source mentions it only in the description of the datasette-embeddings plugin, which stores and queries embedding vectors in Datasette tables. This places the concept within the author's work on making data searchable by similarity. Embedding vectors are the basis for semantic search over stored data. The source does not define the term further.

> "**[datasette-embeddings 0.1a3](https://github.com/datasette/datasette-embeddings/releases/tag/0.1a3)**—2024-04-08  
  Store and query embedding vectors in Datasette tables" — [[sources/2024-04-10-weeknotes-llm-releases_18e6bc]]

## New Information (2024-02-09-weeknotes)

- Embeddings are vector representations of text produced by embedding models. (The source adds that embedding vectors are produced by embedding models, which the existing definition does not state.)
- Embeddings are the basis for semantic search and retrieval, and the source relates them to the planned RAG plugin. (The source extends the existing semantic-search statement to retrieval and links it to the planned llm-rag plugin.)
- The nomic-embed-text-v1 embedding model required a trust-remote-code option in llm-sentence-transformers, added as 'llm sentence-transformers register --trust-remote-code'. (This is a concrete example of embedding models being used through LLM plugins.)
- llm-embed-onnx makes several new embedding models available for use with LLM, running them via ONNX Runtime. (The source names llm-embed-onnx as a related entity that provides embedding models.)
- Retrieval Augmented Generation (The source relates embeddings to Retrieval Augmented Generation through the planned RAG plugin.)

## New Information (2023-10-30-weeknotes)

- Embeddings are numerical vector representations of text, used for search and similarity tasks. (Adds the similarity-task use alongside the existing search characterization, which the page states only in the Description.)
- Embedding models such as the Jina AI 8K text embedding model can be run from the command line through LLM plugins (llm-embed-jina). (This is a concrete real-world usage scenario for embeddings and fits the Applications section.)
- "Embeddings: What they are and why they matter" is a long write-up of the author's PyBay talk on embeddings, and it received heavy traffic as one of the more accessible explanations of what embeddings are. (This is a reference to a source explaining the concept, which fits the Related Content section.)

## New Information (2023-09-17-weeknotes-embeddings)

- Yet another thing you can do with embeddings is use them to find clusters of related items. (Clustering of related items is a concrete usage scenario that the page does not yet list.)
- Embeddings can represent images as well as text; llm-clip generates embeddings for images and text using CLIP, enabling image search. (Image search via CLIP embeddings is a real-world usage scenario not covered by the page's text-only description.)
- Embedding models can now be built as LLM plugins, such as llm-sentence-transformers and llm-clip. (Describes how embedding models are provided and extended in the LLM ecosystem, which fits the page's overview of the concept.)
- Embeddings can be created for structured data, such as all functions in a codebase, by piping symbex output into llm embed-multi and storing the result in a database for CLI-driven semantic search. (A concrete example of building a semantic search engine over embeddings, fitting the Applications section.)

## New Information (2023-01-15-weeknotes)

- Embedding vectors are produced by embedding models, which the page does not state. (Defines how embeddings are generated, a defining trait the page lacks.)
- The GPT-3 embeddings API was named as the source of the vectors used in a documentation Q&A experiment. (A concrete real-world usage of embeddings in a Q&A system over documentation.)
- Embeddings are indexed with FAISS so that similar passages can be retrieved quickly, via datasette-faiss. (A concrete retrieval scenario that fits the page's semantic search application.)
- Yet another thing you can do with embeddings is use them to find clusters of related items. (Clustering of related items is a usage scenario the page does not yet list.)
- llm-clip generates embeddings for images and text using CLIP, enabling image search. (Image search via CLIP embeddings is a usage scenario not covered by the text-only description.)
- Embeddings can be created for structured data, such as all functions in a codebase, by piping symbex output into llm embed-multi and storing them in a database for CLI-driven semantic search. (A concrete example of building a semantic search engine over embeddings.)
- openai-to-sqlite is a command-line tool for storing OpenAI API responses in SQLite, useful for calculating embeddings. (A related tool that the source connects to embedding calculation.)
- Vector similarity search (The source relates embeddings to vector similarity search, a related concept page.)

## Mentions in Source

- "Embedding models can now be [built as LLM plugins](https://llm.datasette.io/en/stable/embeddings/writing-plugins.html)." — [[_Inbox/2023-09-17-weeknotes-embeddings|2023-09-17-weeknotes-embeddings]]
- "Yet another thing you can do with embeddings is use them to find clusters of related items." — [[_Inbox/2023-09-17-weeknotes-embeddings|2023-09-17-weeknotes-embeddings]]
- "[Embeddings: What they are and why they matter](https://simonwillison.net/2023/Oct/23/embeddings/) is the big write-up of my talk about embeddings from PyBay this year." — [[_Inbox/2023-10-30-weeknotes|2023-10-30-weeknotes]]
- "This has received a lot of traffic, presumably because it provides one of the more accessible answers to the question “what are embeddings?”." — [[_Inbox/2023-10-30-weeknotes|2023-10-30-weeknotes]]
- "It makes several new embeddings models available for use with LLM, listed [in the README](https://github.com/simonw/llm-embed-onnx/blob/main/README.md#usage)." — [[_Inbox/2024-02-09-weeknotes|2024-02-09-weeknotes]]
- "How to implement Q&A against your documentation with GPT3, embeddings and Datasette" — [[_Inbox/2023-01-15-weeknotes|2023-01-15-weeknotes]]
- "a command-line tool for storing OpenAI API responses in a SQLite database—useful for calculating embeddings" — [[_Inbox/2023-01-15-weeknotes|2023-01-15-weeknotes]]