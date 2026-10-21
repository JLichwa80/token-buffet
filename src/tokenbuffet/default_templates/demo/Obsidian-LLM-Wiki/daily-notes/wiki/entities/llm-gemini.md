---
type: entity
created: 2026-10-20
updated: 2026-10-20
generation_complete: true
sources:
  - "[[sources/2024-05-28-weeknotes_18b318]]"
  - "[[sources/2024-04-10-weeknotes-llm-releases_18e6bc]]"
tags:
  - "other"
---

# llm-gemini

## Description

llm-gemini is a plugin for [[llm]], the command-line tool, that gives it access to Google's Gemini family of models. It was released as version 0.1a4 on 14 May 2024. The release added support for [[Gemini 1.5 Flash]], which the author describes as a new inexpensive model. The plugin shows how the [[llm]] plugin system extends the tool to new model providers. The author presents it as one of their main releases for the month.

Version 0.1a2 (released 10 April 2024) added support for system prompts, letting users pass instructions alongside the main input from the command line. The REST documentation for sending a system prompt had not yet been updated, so the author reverse-engineered the required format from the Python library. The author recorded those notes in a GitHub issue on the project, and the release serves as a practical example of system prompts in use.

## Related Entities

- [[entities/llm|llm]]
- [[entities/gemini-1-5-flash|Gemini 1.5 Flash]]
- [[entities/google-gemini-pro-1-5|Google Gemini Pro 1.5]]
- [[entities/gpt-4-turbo|GPT-4 Turbo]]
- [[entities/mixtral-8x22b|Mixtral 8x22B]]

## Related Concepts

- [[concepts/large-language-models|Large Language Models]]

## Mentions in Source

- "**[llm-gemini 0.1a2](https://github.com/simonw/llm-gemini/releases/tag/0.1a2)** adds support for them, so now you can do things like this:" — [[_Inbox/2024-04-10-weeknotes-llm-releases|2024-04-10-weeknotes-llm-releases]]
- "LLM plugin to access Google’s Gemini family of models" — [[_Inbox/2024-05-28-weeknotes|2024-05-28-weeknotes]]
- "adding support for the new inexpensive Gemini 1.5 Flash." — [[_Inbox/2024-05-28-weeknotes|2024-05-28-weeknotes]]
- "I had to reverse-engineer the REST format for sending a system prompt from the Python library as the REST documentation hasn’t been updated yet—[notes on that in my issue](https://github.com/simonw/llm-gemini/issues/6#issuecomment-2046460319)." — [[_Inbox/2024-04-10-weeknotes-llm-releases|2024-04-10-weeknotes-llm-releases]]