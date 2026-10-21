---
type: entity
created: 2026-10-21
updated: 2026-10-21
generation_complete: true
sources:
  - "[[sources/2023-12-31-weeknotes_456c53]]"
  - "[[sources/2023-08-05-weeknotes-plugins_fc2660]]"
tags:
  - "other"
  - "project"
aliases:
  - "LLM llama.cpp plugin"
---

# llm-llama-cpp

## Description

llm-llama-cpp is an [[entities/llm|LLM]] plugin for running models through llama.cpp, extending the LLM tool to local model execution. According to the author, it now supports a direct option to load a [[concepts/gguf|GGUF]] model file, which makes it easy to try new models. The plugin's 0.3 release is listed on 2023-12-09. It is one of several LLM plugins that build on the tool's [[concepts/plugins|plugin system]].

llm-llama-cpp was first released as version 0.1a0 on 2023-08-01 as an LLM plugin for running models through llama.cpp. It runs a [[concepts/ggml|GGML]] quantized version of [[entities/llama-2|Llama 2]] directly on the user's own hardware, a step beyond the earlier llm-replicate plugin, which accessed hosted models. Installation uses `llm install llm-llama-cpp llama-cpp-python`. According to the author's 2023-08-05 weeknotes, this plugin is what made it possible to run Llama 2 locally through LLM.

## Related Entities

- [[entities/llm|LLM]]
- [[entities/llama-2|Llama 2]]

## Related Concepts

- [[concepts/gguf|GGUF]]
- [[concepts/plugins|plugin system]]
- [[concepts/ggml|GGML]]
- [[concepts/plugins|Plugins]]

## Mentions in Source

- "* [llm-llama-cpp](https://github.com/simonw/llm-llama-cpp) now supports a `llm -m gguf -o path una-cybertron-7b-v2-bf16.Q8_0.gguf` option, making it much easier to quickly try out a new model distributed as a GGUF file." — [[_Inbox/2023-12-31-weeknotes|2023-12-31-weeknotes]]
- "* **[llm-llama-cpp 0.3](https://github.com/simonw/llm-llama-cpp/releases/tag/0.3)**—2023-12-09  
  LLM plugin for running models using llama.cpp" — [[_Inbox/2023-12-31-weeknotes|2023-12-31-weeknotes]]