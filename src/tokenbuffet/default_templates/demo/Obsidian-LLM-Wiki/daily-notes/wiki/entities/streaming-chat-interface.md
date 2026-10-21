---
type: entity
created: 2026-10-20
updated: 2026-10-20
tags: [topic]
aliases:
  - "streaming chat UI"
  - "Streaming chat interface"
sources:
  - "[[sources/2024-09-06-weeknotes_32f8a8]]"

generation_complete: true
---

# Streaming chat interface

## Description

A streaming chat interface displays an LLM's response incrementally as tokens arrive, rather than waiting for the full reply. In the 2024-09-06 weeknotes, Simon Willison built the [[Gemini Chat App]] partly to experiment with implementing one directly against the [[Gemini]] API from a browser. The experiment shows that client-side JavaScript can handle streamed model output without a server intermediary. It is a technique explored as part of the client-side LLM work, which depends on browsers being allowed to call LLM APIs directly ([[CORS]]).

## Related Entities

- [[entities/gemini-chat-app|Gemini Chat App]]
- [[entities/gemini|Gemini]]

## Related Concepts

- [[concepts/cors|CORS]]

## Mentions in Source

- "I built this partly to try out those new models and partly to experiment with implementing a streaming chat interface agaist the Gemini API directly in a browser." — [[_Inbox/2024-09-06-weeknotes|2024-09-06-weeknotes]]