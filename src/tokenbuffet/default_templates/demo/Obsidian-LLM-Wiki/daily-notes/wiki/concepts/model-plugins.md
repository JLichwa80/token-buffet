---
type: concept
created: 2026-10-21
updated: 2026-10-21
tags: [terminology]
aliases:
  - "LLM model plugins"
  - "Model plugins"
sources:
  - "[[sources/2023-06-27-weeknotes_f6a59b]]"

generation_complete: true
---

# Model plugins

## Definition

Model plugins are a planned category of [[LLM plugins]] for the `llm` tool. Their goal is to let `llm` use language models beyond the OpenAI models it was tied to at the time, such as [[gpt-4]] and GPT-3.5.

## Key Characteristics

- Extends the `llm` tool to non-OpenAI language models.
- One of four plugin categories the author lists as the starting scope for [[LLM plugins]].
- Addresses the limitation that `llm` was tied to OpenAI models at the time.
- A working branch includes an example plugin that calls Google's PaLM 2 model through Google Vertex.
- Planned support for other model families, including models that run locally through llama.cpp.

## Applications

- Calling hosted models from other providers, such as PaLM 2 via Google Vertex, from the `llm` command line tool.
- Running local models, such as those served through llama.cpp, from the same interface.
- Letting users choose among multiple [[LLM]] backends without changing their workflow.

## Related Concepts

- [[concepts/llm-plugins|LLM plugins]]

## Related Entities

- [[entities/llm|LLM]]
- [[entities/gpt-4|gpt-4]]

## Mentions in Source

- "**Model plugins**. I want LLM to be able to use more than just GPT-3.5 and GPT-4." — [[_Inbox/2023-06-27-weeknotes|2023-06-27-weeknotes]]
- "I have a branch with an example plugin that can call Google’s PaLM 2 model via Google Vertex, and I hope to support many other LLM families with additional plugins, including models that can run locally via llama.cpp and similar." — [[_Inbox/2023-06-27-weeknotes|2023-06-27-weeknotes]]