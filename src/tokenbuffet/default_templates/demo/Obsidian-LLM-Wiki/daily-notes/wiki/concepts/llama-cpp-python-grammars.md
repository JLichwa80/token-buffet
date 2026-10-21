---
type: concept
created: 2026-10-21
updated: 2026-10-21
tags: [terminology]
aliases:
  - "llama-cpp grammars"
  - "grammar-constrained decoding"
sources:
  - "[[sources/2023-09-17-weeknotes-embeddings_c2332f]]"

generation_complete: true
---

# llama-cpp-python grammars

## Definition

llama-cpp-python grammars are a feature of llama-cpp that constrains an LLM's output to a specified format, letting the user control the exact structure of the model's output.

## Key Characteristics

- Constrains generated output to a user-specified grammar, so the output follows a defined structure.
- Gives the user direct control over the exact output format, rather than relying on the model to comply through prompting alone.
- Used to produce structured output such as arrays of JSON objects.
- Considered a possible route to an equivalent of [[OpenAI Functions]] for [[Llama 2]] and similar models.

## Applications

- **Structured JSON output:** generating arrays of JSON objects from a local model. Simon Willison used grammars for this purpose, as documented in a TIL dated 2023-09-13.
- **Function-calling equivalent:** Willison is optimistic that grammars could implement behavior similar to [[OpenAI Functions]] for [[Llama 2]] and other open models.

## Related Concepts

- [[concepts/openai-functions|OpenAI Functions]]

## Related Entities

- [[entities/llama-2|Llama 2]]

## Mentions in Source

- "`llama-cpp` has grammars now, which enable you to control the exact output format of the LLM." — [[_Inbox/2023-09-17-weeknotes-embeddings|2023-09-17-weeknotes-embeddings]]