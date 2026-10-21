---
type: entity
created: 2026-10-21
updated: 2026-10-21
generation_complete: true
tags: [organization]
aliases:
  - "openrouter.ai"
sources:
  - "[[sources/2023-08-30-datasette-plus-weeknotes_748a0c]]"

---

# OpenRouter

## Description

OpenRouter is a hosted API service that provides access to many models, including [[Claude]]. In the 2023-08-30 weeknotes, [[Simon Willison]] used it to access Claude while he waited on the official Claude API. The [[llm-openrouter|llm-openrouter]] plugin connects [[LLM|LLM]] to OpenRouter-hosted models. OpenRouter emulates the official OpenAI APIs, including streaming tokens, so LLM can reuse its existing `openai` library code by pointing the `api_base` parameter at OpenRouter. The author notes that Claude's 100,000 token context makes it a strong option for working with large documents.

## Related Entities

- [[entities/llm-openrouter|llm-openrouter]]
- [[entities/anyscale-endpoints|Anyscale Endpoints]]
- [[entities/llm|LLM]]

## Related Concepts

## Mentions in Source

- "Both OpenRouter and Anyscale Endpoints provide API endpoints that emulate the official OpenAI APIs, including the way the handle streaming tokens." — [[_Inbox/2023-08-30-datasette-plus-weeknotes|2023-08-30-datasette-plus-weeknotes]]