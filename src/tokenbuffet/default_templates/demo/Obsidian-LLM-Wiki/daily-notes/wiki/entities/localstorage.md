---
type: entity
created: 2026-10-20
updated: 2026-10-20
tags: [topic]
aliases:
  - "Web Storage API"
  - "browser localStorage"
sources:
  - "[[sources/2024-09-06-weeknotes_32f8a8]]"

generation_complete: true
---

# localStorage

## Description

`localStorage` is a standard Web Storage API mechanism provided by web browsers that allows web applications to store key-value string pairs persistently across page reloads and browser sessions within the same origin. It enables client-side web applications and tools to operate independently without requiring a dedicated backend database for lightweight state and configuration persistence. In client-side developer tooling, it is commonly utilized to cache user credentials, such as an API key for services like [[entities/anthropic|Anthropic]] or [[entities/gemini|Gemini]], after an initial prompt to avoid repeated input. However, because data saved in `localStorage` remains accessible in plain text to any client-side script running in the same origin or anyone with physical access to the browser console, storing sensitive secrets carries inherent security exposure risks.

## Related Entities

- [[entities/anthropic|Anthropic]]
- [[entities/gemini|Gemini]]
- [[entities/datasette|Datasette]]

## Related Concepts

## Mentions in Source

- "I’ve been building tools which `prompt()` a user for their own API key (sadly restricting their usage to the tiny portion of people who both understand API keys and have created API accounts with one of the big providers)—then I stash that key in `localStorage` and start using it to make requests." — [[_Inbox/2024-09-06-weeknotes|2024-09-06-weeknotes]]