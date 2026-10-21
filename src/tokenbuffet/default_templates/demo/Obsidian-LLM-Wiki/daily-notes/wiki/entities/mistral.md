---
type: entity
created: 2026-10-20
updated: 2026-10-21
generation_complete: true
sources:
  - "[[sources/2024-04-10-weeknotes-llm-releases_18e6bc]]"
  - "[[sources/2024-02-27-weeknotes-getting-ready-for-nicar_823782]]"
  - "[[sources/2023-12-31-weeknotes_456c53]]"
tags:
  - "organization"
aliases:
  - "Mistral AI"
---

# Mistral

## Description

Mistral is a French AI company. On April 9, 2024, it released [[Mixtral 8x22B]] by tweeting a BitTorrent magnet link, at 3:20am in France, its home country. The company's releases are openly licensed models, which the source contrasts with its earlier [[Mixtral 8x7B]]. In the source's 24-hour review, Mistral is one of three major LLM releases, alongside [[Google Gemini Pro 1.5]] and [[GPT-4 Turbo]].

Mistral released Mistral Large on the morning of 2024-02-27, the day of the source post, and the author rushed out a new llm-mistral plugin release to add support for it. Mistral's API is also the endpoint the llm-mistral plugin uses to give the LLM tool access to Mistral models, so Mistral is a model provider as well as a model releaser. The plugin reads Mistral's API model-list endpoint through a cache, so future Mistral models work without a new plugin release.

The llm-mistral 0.2 release from 2023-12-15 is not in the existing section, so the new fact is appended:

llm-mistral 0.2 was released on 2023-12-15 as an LLM plugin providing access to Mistral models through the Mistral API. It is the earliest llm-mistral release noted on this page.
## Related Entities

- [[entities/google-gemini-pro-1-5|Google Gemini Pro 1.5]]
- [[entities/gpt-4-turbo|GPT-4 Turbo]]
- [[entities/mixtral-8x22b|Mixtral 8x22B]]

## Related Concepts

## Mentions in Source

- "Mistral released Mistral Large this morning, so I rushed out a new release of my llm-mistral plugin to add support for it." — [[_Inbox/2024-02-27-weeknotes-getting-ready-for-nicar|2024-02-27-weeknotes-getting-ready-for-nicar]]
- "The plugin now hits the Mistral API endpoint that lists models (via a cache), which means future model releases should be supported automatically without needing a new plugin release." — [[_Inbox/2024-02-27-weeknotes-getting-ready-for-nicar|2024-02-27-weeknotes-getting-ready-for-nicar]]
- "6:20pm (3:20am in their home country of France): Mistral [tweet a link](https://twitter.com/MistralAI/status/1777869263778291896) to a 281GB magnet BitTorrent of **Mixtral 8x22B**—their latest openly licensed model release, significantly larger than their previous best open model Mixtral 8x7B." — [[_Inbox/2024-04-10-weeknotes-llm-releases|2024-04-10-weeknotes-llm-releases]]
- "* [Many options for running Mistral models in your terminal using LLM](https://simonwillison.net/2023/Dec/18/mistral/), demonstrating how LLM’s plugins system has really started to pay off." — [[_Inbox/2023-12-31-weeknotes|2023-12-31-weeknotes]]
- "* **[llm-mistral 0.2](https://github.com/simonw/llm-mistral/releases/tag/0.2)**—2023-12-15  
  LLM plugin providing access to Mistral models busing the Mistral API" — [[_Inbox/2023-12-31-weeknotes|2023-12-31-weeknotes]]