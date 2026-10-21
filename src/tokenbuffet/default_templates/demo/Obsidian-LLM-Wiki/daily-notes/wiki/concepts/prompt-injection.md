---
type: concept
created: 2026-10-20
updated: 2026-10-21
generation_complete: true
sources:
  - "[[sources/2024-04-10-weeknotes-llm-releases_18e6bc]]"
  - "[[sources/2023-12-31-weeknotes_456c53]]"
  - "[[sources/2023-05-10-weeknotes_35d224]]"
  - "[[sources/2023-05-01-weeknotes_72fe7e]]"
tags:
  - "terminology"
aliases:
  - "prompt injection attack"
---

# prompt injection

## Definition

Prompt injection is the risk that malicious input within a prompt overrides the instructions an LLM was given. A system prompt is not a guaranteed defense: even when instructions are separated from data by a system prompt, they can still be overridden by content in the main prompt.

## Key Characteristics

- Malicious input is placed inside the prompt and is treated as instructions by the model.
- The attacker's text can override the developer's original instructions.
- Separating instructions from data with a system prompt does not reliably prevent it.
- It is a risk for any application that passes untrusted text to an LLM.
- You can't solve AI security problems with more AI. Simon Willison restated this argument in the source's note on the LangChain prompt injection webinar.
## Applications

- Evaluating the security of LLM-based applications that process untrusted user input.
- Designing defenses for LLM systems, with the understanding that system prompts alone are insufficient.
- Assessing the potential impact of LLM misuse, as discussed in the source's earlier post on the worst outcomes of this risk.
- Mitigating prompt injection by limiting the blast radius: reducing what a compromised model can access or do. This recommendation comes from a RedMonk Conversations podcast episode the author recorded with Kate Holterhoff.
## Related Concepts

- [[concepts/dual-llm-pattern|Dual LLM pattern]]

## Related Entities

- [[entities/google-gemini-pro-1-5|Google Gemini Pro 1.5]]
- [[entities/gpt-4-turbo|GPT-4 Turbo]]
- [[entities/mixtral-8x22b|Mixtral 8x22B]]

## Mentions in Source

- "I participated in the LangChain webinar about prompt injection. The session was recorded, so I extracted my 12 minute introduction to the topic and turned it into [a blog post](https://simonwillison.net/2023/May/2/prompt-injection-explained/) complete with a Whisper transcription, a video and the slides I used in the talk." — [[_Inbox/2023-05-10-weeknotes|2023-05-10-weeknotes]]
- "* [Recommendations to help mitigate prompt injection: limit the blast radius](https://simonwillison.net/2023/Dec/20/mitigate-prompt-injection/), extracted from a podcast episode I recorded with Kate Holterhoff for RedMonk Conversations." — [[_Inbox/2023-12-31-weeknotes|2023-12-31-weeknotes]]
- "They’re sadly [not a guaranteed solution for prompt injection](https://simonwillison.net/2023/Apr/14/worst-that-can-happen/#gpt4)—even with instructions separated from data by a system prompt you can still over-ride them in the main prompt if you try hard enough—but they’re still useful for non-adversarial situations." — [[_Inbox/2024-04-10-weeknotes-llm-releases|2024-04-10-weeknotes-llm-releases]]
- "My other blog entry this week introduced [The Dual LLM pattern for building AI assistants that can resist prompt injection](https://simonwillison.net/2023/Apr/25/dual-llm-pattern/)—my latest thinking on how we might be able to build AI assistants even without a robust solution to the prompt injection problem." — [[_Inbox/2023-05-01-weeknotes|2023-05-01-weeknotes]]