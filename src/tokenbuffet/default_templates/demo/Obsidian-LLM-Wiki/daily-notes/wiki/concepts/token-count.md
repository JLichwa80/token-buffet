---
type: concept
created: 2026-10-21
updated: 2026-10-21
tags: [terminology]
aliases:
  - "token efficiency"
  - "Token count"
sources:
  - "[[sources/2023-06-27-weeknotes_f6a59b]]"

generation_complete: true
---

# Token count

## Definition

Token count is the number of tokens a language model reads in its input. In the source, it is the main constraint when text is piped into a model, and the goal is to give the model the shortest text that still lets it produce useful results.

## Key Characteristics

- Treated as the primary constraint when piping code or text into a language model.
- Drives a minimal-input principle: provide the shortest amount of text that gives the model enough to produce interesting results.
- Shaped the design of [[symbex]]'s signature output (`-s`/`--signatures`), which omits function bodies to reduce the tokens sent to the model.
- The source does not define tokens in detail and refers readers to the author's separate writing on tokenizers for background.

## Applications

- Choosing what to send to a model when extracting code: printing only function or class signatures instead of full bodies.
- Designing command-line tools whose output will be piped into an LLM, so that output stays small.
- Judging whether a given input fits within a model's context limit.

## Related Concepts

## Related Entities

- [[entities/symbex|symbex]]

## Mentions in Source

- "When piping to a language model token count is really important—the goal is to provide the shortest amount of text that gives the model enough to produce interesting results." — [[_Inbox/2023-06-27-weeknotes|2023-06-27-weeknotes]]