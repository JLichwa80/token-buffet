---
type: entity
created: 2026-10-21
sources:
  - "[[sources/2023-10-30-weeknotes_d4a215]]"
tags: [other]
stub: true
generation_complete: true
---
# PyTorch

> Stub created by the ingest candidate gate (prose+named) — [[sources/2023-10-30-weeknotes_d4a215]] names this without treating it. Will be filled by the next ingest of a source that does.

PyTorch is a machine learning library that some LLM plugins depend on. At the time of the post it was not yet available for Python 3.12. This caused plugin installation failures for users whose LLM was installed from the newly upgraded Homebrew package. The author's new llm-embed-jina plugin was one of the affected plugins. The incompatibility motivated the creation of the llm-python plugin for debugging environment issues.

> "This means that while base LLM installed from Homebrew works fine, attempts to install things like my new [llm-embed-jina](https://github.com/simonw/llm-embed-jina) plugin fail with [weird errors](https://github.com/simonw/llm-embed-jina/issues/5)." — [[sources/2023-10-30-weeknotes_d4a215]]
