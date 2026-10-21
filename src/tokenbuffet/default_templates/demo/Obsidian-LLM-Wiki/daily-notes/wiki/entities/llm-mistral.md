---
type: entity
created: 2026-10-21
updated: 2026-10-21
tags: [project]
aliases:
  - "llm-mistral plugin"
sources:
  - "[[sources/2024-02-27-weeknotes-getting-ready-for-nicar_823782]]"

generation_complete: true
---

# llm-mistral

## Description

llm-mistral is an [[LLM]] plugin that provides access to [[Mistral]] models through the Mistral API. Version 0.3 was released on 2024-02-26 to add support for Mistral Large on the day it launched. The plugin fetches the model list from the Mistral API through a cache, so new Mistral models work without a new plugin release. Usage is set up with the `llm install` and `llm keys` commands. The plugin is an example of the author's approach to keeping LLM integrations current.

## Related Entities

- [[entities/mistral|Mistral]]

## Related Concepts

## Mentions in Source

- "The plugin now hits the Mistral API endpoint that lists models (via a cache), which means future model releases should be supported automatically without needing a new plugin release." — [[_Inbox/2024-02-27-weeknotes-getting-ready-for-nicar|2024-02-27-weeknotes-getting-ready-for-nicar]]