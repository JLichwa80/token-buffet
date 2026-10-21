---
type: concept
created: 2026-10-21
updated: 2026-10-21
tags: [terminology]
aliases:
  - "GGML quantized model"
  - "GGML format"
sources:
  - "[[sources/2023-08-05-weeknotes-plugins_fc2660]]"

generation_complete: true
---

# GGML

## Definition

GGML is a file format and library for storing quantized model weights. Quantization reduces the numerical precision of model weights to lower their memory footprint, which allows large models such as [[Large Language Model|large language models]] to run on consumer hardware.

## Key Characteristics

- Stores quantized model weights, trading some numerical precision for lower memory use.
- Enables local inference, so models can run on a user's own machine rather than a hosted service.
- Serves as the model format consumed by the llama.cpp-based plugin [[llm-llama-cpp]].

## Applications

- Running a GGML-quantized [[Llama 2]] model locally through [[llm-llama-cpp]], as described in Simon Willison's 5 August 2023 weeknotes.
- Making large models usable on consumer hardware, where full-precision weights would exceed available memory.

## Related Concepts

- [[concepts/large-language-models|Large Language Model]]

## Related Entities

- [[entities/llm-llama-cpp|llm-llama-cpp]]
- [[entities/llama-2|Llama 2]]

## Mentions in Source

- "A few days ago I took that a step further: the new [llm-llama-cpp](https://github.com/simonw/llm-llama-cpp) plugin can now be used to run a GGML quantized version of the Llama 2 model directly on your own hardware." — [[_Inbox/2023-08-05-weeknotes-plugins|2023-08-05-weeknotes-plugins]]