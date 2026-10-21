---
type: entity
created: 2026-10-21
updated: 2026-10-21
generation_complete: true
sources:
  - "[[sources/2023-12-31-weeknotes_456c53]]"
  - "[[sources/2023-08-30-datasette-plus-weeknotes_748a0c]]"
tags:
  - "other"
---

# Anyscale Endpoints

> Stub created by the ingest candidate gate (prose+named) — [[sources/2023-12-31-weeknotes_456c53]] names this without treating it. Will be filled by the next ingest of a source that does.

Anyscale Endpoints is a hosted service that serves machine learning models. In this source it is the backend for the llm-anyscale-endpoints plugin, which lets the LLM command-line tool call models hosted there. The llm-anyscale-endpoints 0.4 release is listed among the December 2023 releases, dated 2023-12-14. The source does not describe the service itself beyond its role as a model host. It sits alongside the Mistral and Gemini plugins as another hosted-model provider reachable through the LLM plugin system.

> "**[llm-anyscale-endpoints 0.4](https://github.com/simonw/llm-anyscale-endpoints/releases/tag/0.4)**—2023-12-14  
  LLM plugin for models hosted by Anyscale Endpoints" — [[sources/2023-12-31-weeknotes_456c53]]

## New Information (2023-08-30-datasette-plus-weeknotes)

- Anyscale Endpoints is a hosted API service that provides Llama 2 and Code Llama at very low prices, between $0.25 and $1 per million tokens depending on the model. (This describes what the service offers and its pricing, which the existing description lacks.)
- Anyscale Endpoints emulates the official OpenAI APIs, including the way it handles streaming tokens, so the llm-anyscale-endpoints plugin can reuse LLM's OpenAI-compatible code (under 30 lines). (This explains how the service is integrated, a defining trait of the service.)
- llm-anyscale-endpoints 0.2 was released on 2023-08-25 as an LLM plugin for models hosted by Anyscale Endpoints. (This adds an earlier plugin release date to the page's release history.)

## Mentions in Source

- "Anyscale provide Llama 2 and Code Llama at extremely low prices—between $0.25 and $1 per million tokens, depending on the model." — [[_Inbox/2023-08-30-datasette-plus-weeknotes|2023-08-30-datasette-plus-weeknotes]]
- "Both OpenRouter and Anyscale Endpoints provide API endpoints that emulate the official OpenAI APIs, including the way the handle streaming tokens." — [[_Inbox/2023-08-30-datasette-plus-weeknotes|2023-08-30-datasette-plus-weeknotes]]