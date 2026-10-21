---
type: entity
created: 2026-10-20
updated: 2026-10-21
generation_complete: true
sources:
  - "[[sources/2024-09-06-weeknotes_32f8a8]]"
  - "[[sources/2023-12-31-weeknotes_456c53]]"
tags:
  - "other"
aliases:
  - "Google Gemini"
  - "Gemini Pro"
---

# Gemini

## Description

Gemini is Google's family of large language models. In the 2024-09-06 weeknotes, the author uses the Gemini 1.5 Pro and Flash APIs as the model behind several of his experiments. He considers Gemini Pro the only vision LLM he has tried with reliable support for [[Bounding boxes]], and he built the gemini-bbox tool on that capability. He also used Gemini 1.5 Pro to convert PDFs into HTML and Markdown, and built the Gemini Chat App on the Gemini API, which he mentions alongside the new gemini-1.5-flash-8b-exp-0827 model. Unlike [[Anthropic]]'s API, which needs a special request header for browser calls, Gemini supports CORS without it, which makes direct client-side access possible.

## Related Entities

- [[entities/anthropic|Anthropic]]
- [[entities/datasette|Datasette]]

## Related Concepts

- [[concepts/bounding-boxes|Bounding boxes]]

## Mentions in Source

- "I’ve spent less than a total of ten minutes on using Gemini to convert PDFs in this way and the results have been very impressive." — [[_Inbox/2024-09-06-weeknotes|2024-09-06-weeknotes]]
- "I bet you could build that whole thing as a client-side app against the Gemini Pro API, too..." — [[_Inbox/2024-09-06-weeknotes|2024-09-06-weeknotes]]