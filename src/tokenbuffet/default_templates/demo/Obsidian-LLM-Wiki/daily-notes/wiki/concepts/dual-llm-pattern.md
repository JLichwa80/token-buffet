---
type: concept
created: 2026-10-21
updated: 2026-10-21
tags: [idea]
aliases:
  - "Dual LLM"
sources:
  - "[[sources/2023-05-01-weeknotes_72fe7e]]"

generation_complete: true
---

# Dual LLM pattern

## Definition

The Dual LLM pattern is a proposed design for AI assistants that aims to resist [[Prompt injection]]. It was introduced by Simon Willison in a blog entry from the week before the 2023-05-01 weeknotes. Willison presents it as his latest thinking on how assistants might be built without a robust solution to the prompt injection problem. The source describes it as a proposal rather than a finished solution.

## Key Characteristics

- Designed to make AI assistants resistant to prompt injection.
- Presented as a proposal, not a finished or proven solution.
- Positioned as an answer to the lack of a robust general fix for prompt injection.
- Described in more detail in a separate post linked from the originating blog entry.

## Applications

- Building AI assistants that process untrusted input (for example, text from emails or web pages) while limiting the influence of injected instructions.
- Serving as a reference design for discussing how assistant architectures might separate or isolate model roles to reduce prompt injection risk.

## Related Concepts

- [[concepts/prompt-injection|Prompt injection]]

## Related Entities

## Mentions in Source

- "My other blog entry this week introduced [The Dual LLM pattern for building AI assistants that can resist prompt injection](https://simonwillison.net/2023/Apr/25/dual-llm-pattern/)—my latest thinking on how we might be able to build AI assistants even without a robust solution to the prompt injection problem." — [[_Inbox/2023-05-01-weeknotes|2023-05-01-weeknotes]]