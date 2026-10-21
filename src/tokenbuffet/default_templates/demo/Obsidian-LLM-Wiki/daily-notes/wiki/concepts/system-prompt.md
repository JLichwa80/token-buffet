---
type: concept
created: 2026-10-20
updated: 2026-10-20
tags: [terminology]
aliases:
  - "system prompts"
sources:
  - "[[sources/2024-04-10-weeknotes-llm-releases_18e6bc]]"

generation_complete: true
---

# system prompt

## Definition

A system prompt is an extra prompt passed to a large language model (LLM) alongside the main input, giving it instructions about how to process that input. The source notes that system prompts are not a guaranteed defense against prompt injection, but remain useful in non-adversarial situations.

## Key Characteristics

- Supplied in addition to the main input and used to steer how that input is processed.
- Not a reliable security boundary: instructions can still be overridden by a sufficiently determined main prompt.
- Effective for non-adversarial use, where the goal is to shape output rather than resist hostile input.
- Support varies by provider. The source reports that [[Google Gemini Pro 1.5]] gained system prompt support, and that `llm-gemini` 0.1a2 exposed it through the command line.
- Can change output behavior. The source's example uses a system prompt of "in spanish", which changes the output language.

## Applications

- Setting the response language or tone for every request in a session.
- Giving an LLM a fixed role or processing rules separate from the data it receives.
- Shaping output format or style in tools that call models through a command line or API.

## Related Concepts

## Related Entities

- [[entities/google-gemini-pro-1-5|Google Gemini Pro 1.5]]
- [[entities/gpt-4-turbo|GPT-4 Turbo]]
- [[entities/mixtral-8x22b|Mixtral 8x22B]]

## Mentions in Source

- "I really like system prompts—extra prompts you can pass to an LLM that give it instructions about how to process the main input." — [[_Inbox/2024-04-10-weeknotes-llm-releases|2024-04-10-weeknotes-llm-releases]]