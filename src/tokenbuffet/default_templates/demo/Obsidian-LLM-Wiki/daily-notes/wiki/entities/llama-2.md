---
type: entity
created: 2026-10-21
updated: 2026-10-21
generation_complete: true
sources:
  - "[[sources/2023-08-30-datasette-plus-weeknotes_748a0c]]"
  - "[[sources/2023-08-16-datasette-cloud-weeknotes_9ee111]]"
  - "[[sources/2023-08-05-weeknotes-plugins_fc2660]]"
tags:
  - "other"
---

# Llama 2

> Stub created by the ingest candidate gate (prose+named) — [[sources/2023-08-30-datasette-plus-weeknotes_748a0c]] names this without treating it. Will be filled by the next ingest of a source that does.

Llama 2 is a large language model that appears in the source as one of the models hosted by Anyscale Endpoints. Willison notes that Anyscale offers it at very low prices, between $0.25 and $1 per million tokens depending on the model. Its role in the source is as an example of the open models that the llm-anyscale-endpoints plugin makes accessible through the LLM CLI. It is mentioned in passing alongside Code Llama, and the source does not discuss its internals. It connects to the llm-anyscale-endpoints and Anyscale Endpoints entries already extracted from this source.

> "Anyscale provide Llama 2 and Code Llama at extremely low prices—between $0.25 and $1 per million tokens, depending on the model." — [[sources/2023-08-30-datasette-plus-weeknotes_748a0c]]

## New Information (2023-08-16-datasette-cloud-weeknotes)

- Llama 2 can be run locally on an Apple Silicon Mac with GPU acceleration using the llm-mlc plugin for LLM, which the author describes as possibly one of the easiest ways to do so. (This adds a concrete local-usage scenario for Llama 2 that fits the Applications section.)
- The Llama-2-7b-chat variant is downloaded with `llm mlc download-model Llama-2-7b-chat --alias llama2`, after which prompts can be run against it through the llama2 alias. (This documents a specific usage workflow for running Llama 2 through the LLM CLI, which belongs with the other application details.)

## New Information (2023-08-05-weeknotes-plugins)

- Llama 2 is the first commercially usable version of Meta's LLaMA language model, released on July 18th (2023). (The 2023-08-05 source gives the release date and commercial-usability status, which the page's description does not include.)
- Llama 2 could be prompted through the LLM CLI on its launch morning via the llm-replicate plugin, which the author had released the day before the launch. (This describes a concrete usage scenario of prompting Llama 2 from the command line through a plugin, which fits the Applications section.)
- The llm-llama-cpp plugin can run a GGML quantized version of Llama 2 (llama-2-7b-chat) directly on the user's own hardware, installable via Homebrew-packaged LLM. (This adds a local-execution usage scenario using GGML quantization, which belongs with the other application details.)

## Mentions in Source

- "For a while now I’ve been trying to work out the easiest recipe to get a Llama 2 model running on my M2 Mac with GPU acceleration." — [[_Inbox/2023-08-16-datasette-cloud-weeknotes|2023-08-16-datasette-cloud-weeknotes]]
- "And finally, you can download the Llama 2 model using this command:" — [[_Inbox/2023-08-16-datasette-cloud-weeknotes|2023-08-16-datasette-cloud-weeknotes]]
- "The timing on this could not have been better: [Llama 2](https://ai.meta.com/llama/) (the first commercially usable version of Meta’s LLaMA language model) was released on July 18th, and I was able to add support to prompting it via LLM that very morning thanks to [the llm-replicate plugin](https://simonwillison.net/2023/Jul/18/accessing-llama-2/) I had released the day before that launch." — [[_Inbox/2023-08-05-weeknotes-plugins|2023-08-05-weeknotes-plugins]]