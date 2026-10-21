---
type: entity
created: 2026-10-21
updated: 2026-10-21
tags: [project]
aliases:
  - "ttok 0.2"
sources:
  - "[[sources/2023-07-16-weeknotes_8e11f0]]"

generation_complete: true
---

# ttok

## Description

ttok is a command-line tool written by [[Simon Willison]] for counting tokens, the units that large language models such as GPT-4 process. Version 0.2, released on 2023-07-10, adds `--encode` and `--decode` options so users can see the token IDs for a string and convert those IDs back into text. Willison's demo shows that `Hello world` produces 2 tokens, and that the encoded output (`9906 1917`) can be decoded back to `Hello world`. With `--tokens`, the encoded output includes whitespace-prefixed tokens such as `b' world'`. Willison links the feature to his earlier writing on GPT tokenization, and the 0.2 release is listed in the weeknotes as a utility that counts and truncates text based on tokens. ttok is a separate tool from [[LLM]], although both concern large language models.

## Related Entities

- [[entities/llm|LLM]]

## Related Concepts

## Mentions in Source

- "ttok is my CLI tool for counting tokens, as used by LLM models such as GPT-4." — [[_Inbox/2023-07-16-weeknotes|2023-07-16-weeknotes]]
- "ttok 0.2 adds a requested feature to help make tokens easier to understand, best illustrated by this demo:" — [[_Inbox/2023-07-16-weeknotes|2023-07-16-weeknotes]]