---
type: concept
created: 2026-10-21
updated: 2026-10-21
tags: [terminology]
aliases:
  - "GGUF file format"
sources:
  - "[[sources/2023-12-31-weeknotes_456c53]]"

generation_complete: true
---

# GGUF

## Definition

GGUF is a file format for distributing machine learning models. It is used with tools based on llama.cpp.

## Key Characteristics

- Packages a model for distribution in a single file, such as `una-cybertron-7b-v2-bf16.Q8_0.gguf`.
- Is supported by llama.cpp-based tools, including the [[llm-llama-cpp]] plugin for [[LLM]].
- Lets a user load a model directly with a file path (for example, the `-m gguf` option), without a more complex setup.

## Applications

- Running local models in the [[LLM]] ecosystem: the [[llm-llama-cpp]] plugin accepts a GGUF file through the `-m gguf` option, so a user can quickly try a new model.
- Distributing quantized models: the example model `una-cybertron-7b-v2-bf16.Q8_0.gguf` is distributed in this format.

## Related Concepts

- [[concepts/plugin-system|plugin system]]

## Related Entities

- [[entities/llm-llama-cpp|llm-llama-cpp]]
- [[entities/llm|LLM]]

## Mentions in Source

- "* [llm-llama-cpp](https://github.com/simonw/llm-llama-cpp) now supports a `llm -m gguf -o path una-cybertron-7b-v2-bf16.Q8_0.gguf` option, making it much easier to quickly try out a new model distributed as a GGUF file." — [[_Inbox/2023-12-31-weeknotes|2023-12-31-weeknotes]]