---
created: 2026-10-20
updated: 2026-10-21
generation_complete: true
sources:
  - "[[sources/2024-09-06-weeknotes_32f8a8]]"
  - "[[sources/2024-04-23-weeknotes_a3933c]]"
  - "[[sources/2023-03-22-weeknotes_1bbf6a]]"
tags:
---

type: entity
created: 2026-10-20
updated: 2026-10-20
sources: ["[[sources/2024-09-06-weeknotes_32f8a8]]"]
tags: [organization]
aliases: ["Anthropic AI"]
---

# Anthropic

## Description

Anthropic is the AI company that builds the Claude family of large language models and exposes them through the Claude APIs. As of the 2024-09-06 weeknotes, it had recently added CORS support to those APIs, allowing browser JavaScript to call Claude directly. Using this requires a special request header, `anthropic-dangerous-direct-browser-access: true`, which the author describes as awkward. The author relies on Anthropic's models in his own tools, including a Claude 3 Haiku demo and code written with Claude 3.5 Sonnet and Claude 3 Opus. Anthropic is therefore both an enabler of the client-side approach ([[CORS]]) and the provider of the models behind the author's AI-assisted development work. Other browser-accessible LLM APIs in the same source include [[Gemini]].

## Related Entities

- [[entities/gemini|Gemini]]
- [[entities/datasette|Datasette]]

## Related Concepts

- [[concepts/cors|CORS]]

## Mentions in Source

- "Anthropic [recently added CORS support](https://simonwillison.net/2024/Aug/23/anthropic-dangerous-direct-browser-access/) to their Claude APIs. It’s a little hard to use—you have to add `anthropic-dangerous-direct-browser-access: true` to your request headers to enable it—but once you know the trick you can start building web applications that talk to Anthropic’s LLMs directly, without any additional server-side code." — [[_Inbox/2024-09-06-weeknotes|2024-09-06-weeknotes]]