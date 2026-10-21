---
created: 2026-10-21
updated: 2026-10-21
sources:
  - "[[sources/2023-07-16-weeknotes_8e11f0]]"

generation_complete: true
---

type: concept
created: 2026-10-21
updated: 2026-10-21
sources: ["[[sources/2023-07-16-weeknotes_8e11f0]]"]
tags: [reference]
aliases: ["LLM model plugin tutorial", "Model plugin tutorial"]
---

# Writing a plugin to support a new model

## Definition

"Writing a plugin to support a new model" is a tutorial in the [[LLM]] documentation that explains how to add a new language model to the LLM tool as a plugin. It is the documentation counterpart to the LLM plugin architecture and is intended to let others build and release their own model plugins.

## Key Characteristics

- Documents how to add a new language model to LLM through the plugin system, rather than only the built-in OpenAI models.
- Written by the LLM author because comprehensive documentation for generative AI was scarce.
- Describes how to package a model plugin for release.
- Was written while the author researched how to package plugins, including building a Python package from a `pyproject.toml` file alone.
- Existing model plugins that follow this pattern include [[llm-gpt4all]], [[llm-palm]], and [[llm-mpt30b]].

## Applications

- Adding a self-hosted or third-party language model to LLM, so it works alongside OpenAI models through the same interface.
- Building and publishing a model plugin that others can install.
- Serving as a reference for the plugin architecture when developing new LLM integrations.

## Related Concepts

## Related Entities

- [[entities/llm|LLM]]
- [[entities/llm-gpt4all|llm-gpt4all]]
- [[entities/llm-palm|llm-palm]]
- [[entities/llm-mpt30b|llm-mpt30b]]

## Mentions in Source

- "Comprehensive documentation is sorely lacking in the world of generative AI. I’ve decided to push back against that for LLM, so I spent a bunch of time working on an extremely comprehensive tutorial for writing a plugin that adds a new language model to the tool:" — [[_Inbox/2023-07-16-weeknotes|2023-07-16-weeknotes]]