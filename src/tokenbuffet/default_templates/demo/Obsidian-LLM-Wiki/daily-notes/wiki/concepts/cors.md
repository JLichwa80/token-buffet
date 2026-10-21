---
type: concept
created: 2026-10-20
updated: 2026-10-20
tags: [terminology]
aliases:
  - "Cross-Origin Resource Sharing"
sources:
  - "[[sources/2024-09-06-weeknotes_32f8a8]]"

generation_complete: true
---

# CORS

## Definition

CORS (Cross-Origin Resource Sharing) is a browser mechanism that controls whether a web page may make requests to APIs on a different domain (origin) than the one that served the page.

## Key Characteristics

- Enforced by the browser, not by the server receiving the request.
- Governs cross-origin requests made from client-side JavaScript.
- The server opts in by returning response headers that allow the requesting origin.
- Some providers support CORS by default, while others require an additional request header to enable it.
- Required for a web page to call a third-party API directly from the browser.

## Applications

- Calling LLM APIs directly from client-side JavaScript in a web page. The post describes CORS support as the technical prerequisite for this approach.
- Comparing API providers: the post notes that [[Gemini]] already supports CORS without an extra header, while [[Anthropic]] added support recently but requires a special request header, which the author finds somewhat hard to use.

## Related Concepts

## Related Entities

- [[entities/anthropic|Anthropic]]
- [[entities/gemini|Gemini]]

## Mentions in Source

- "I later found out that both OpenAI and Google Gemini have this capability too, without needing the special header." — [[_Inbox/2024-09-06-weeknotes|2024-09-06-weeknotes]]
- "I’ve been having a bunch of fun taking advantage of CORS-enabled LLM APIs to build client-side JavaScript applications that access LLMs directly." — [[_Inbox/2024-09-06-weeknotes|2024-09-06-weeknotes]]