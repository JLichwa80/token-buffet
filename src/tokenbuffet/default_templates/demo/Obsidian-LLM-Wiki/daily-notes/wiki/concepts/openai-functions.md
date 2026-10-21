---
type: concept
created: 2026-10-21
updated: 2026-10-21
generation_complete: true
sources:
  - "[[sources/2023-09-17-weeknotes-embeddings_c2332f]]"
  - "[[sources/2023-06-27-weeknotes_f6a59b]]"
tags:
  - "terminology"
aliases:
  - "Function calling"
  - "OpenAI function calling"
  - "OpenAI functions mechanism"
---

# OpenAI Functions

## Definition

OpenAI Functions is an OpenAI API feature that makes a model return structured, function-call style output, such as a named function and JSON-formatted arguments, instead of free-form text. In the source, Simon Willison cites it only as a reference point: the benchmark he wants to match with [[llama-cpp-python grammars]] running on open models.

## Key Characteristics

- Produces structured output (function name and arguments) rather than unconstrained text
- Is provided as a hosted feature of the OpenAI API
- Serves as the reference behavior that open-model tooling aims to reproduce
- Enables programmatic parsing of model output without manual post-processing

## Applications

- Calling external tools or APIs from a language model based on natural-language requests
- Extracting structured data (such as JSON records) from unstructured text
- Benchmarking structured-output methods for locally run or open-weight models, as in the source's comparison with llama-cpp grammars
- Serves as the technical foundation for function plugins in Simon Willison's LLM command-line tool, which would let installed plugins add new functions that the model can execute. As of the 2023-06-27 weeknotes, this was still under development, so the plugin category depended on getting the integration working first.
## Related Concepts

- [[concepts/llama-cpp-python-grammars|llama-cpp-python grammars]]

## Related Entities

## Mentions in Source

- "I’m optimistic that these could be used to implement an equivalent to OpenAI Functions on top of Llama 2 and similar models." — [[_Inbox/2023-09-17-weeknotes-embeddings|2023-09-17-weeknotes-embeddings]]
- "Once I get the new OpenAI functions mechanism working, I’d like to be able to install plugins that make new functions available to be executed by the LLM!" — [[_Inbox/2023-06-27-weeknotes|2023-06-27-weeknotes]]