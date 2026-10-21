---
type: entity
created: 2026-10-21
updated: 2026-10-21
tags: [project]
aliases:
  - "llm-openrouter 0.1"
sources:
  - "[[sources/2023-08-30-datasette-plus-weeknotes_748a0c]]"

generation_complete: true
---

# llm-openrouter

## Description

llm-openrouter is an [[LLM]] plugin, released as version 0.1 on 2023-08-21, that provides access to models hosted by [[OpenRouter]]. Its core code is under 30 lines because it reuses LLM's existing OpenAI-compatible library integration, since OpenRouter emulates the official OpenAI APIs. [[Simon Willison]] built it quickly and used it to access Claude while he waited for official Claude API access. It is a key example of the weeknotes' theme of easy plugin development, and it was published alongside [[llm-anyscale-endpoints]].

## Related Entities

- [[entities/openrouter|OpenRouter]]
- [[entities/llm|LLM]]
- [[entities/llm-anyscale-endpoints|llm-anyscale-endpoints]]

## Related Concepts

## Mentions in Source

- "I released two new plugins for [LLM](https://llm.datasette.io/), which lets you run large language models either locally or via APIs, as both a CLI tool and a Python library." — [[_Inbox/2023-08-30-datasette-plus-weeknotes|2023-08-30-datasette-plus-weeknotes]]
- "These plugins were very quick to develop." — [[_Inbox/2023-08-30-datasette-plus-weeknotes|2023-08-30-datasette-plus-weeknotes]]