---
type: entity
created: 2026-10-21
updated: 2026-10-21
tags: [other]
aliases:
  - "llm-embed-jina plugin"
sources:
  - "[[sources/2023-10-30-weeknotes_d4a215]]"

generation_complete: true
---

# llm-embed-jina

## Description

llm-embed-jina is a plugin for the [[LLM]] command-line tool that runs the [[Jina AI]] 8K text embedding model. The author released version 0.1.2 on 2023-10-26. Installation was affected by the Homebrew Python 3.12 upgrade and by missing [[PyTorch]] support. The author wrote a related blog post about executing Jina embeddings from the command line. It is one of the embedding-focused tools in the author's LLM ecosystem, alongside the [[Embeddings]] functionality it exposes through LLM.

## Related Entities

- [[entities/llm|LLM]]
- [[entities/jina-ai|Jina AI]]
- [[entities/pytorch|PyTorch]]

## Related Concepts

- [[concepts/embedding-vector|Embeddings]]

## Mentions in Source

- "In [Execute Jina embeddings with a CLI using llm-embed-jina](https://simonwillison.net/2023/Oct/26/llm-embed-jina/) I released [a new plugin](https://github.com/simonw/llm-embed-jina) to run the new Jina AI 8K text embedding model using my [LLM](https://llm.datasette.io/) command-line tool." — [[_Inbox/2023-10-30-weeknotes|2023-10-30-weeknotes]]