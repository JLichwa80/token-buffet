---
type: concept
created: 2026-10-21
updated: 2026-10-21
tags: [terminology]
aliases:
  - "Magic parameter"
sources:
  - "[[sources/2023-01-15-weeknotes_aefc7f]]"

generation_complete: true
---

# Magic parameters

## Definition

Magic parameters are [[Datasette]] query parameters whose values are filled in automatically from the environment rather than typed by the user. Because the value comes from the environment, a secret such as an API key can be supplied without appearing in the URL. The [[datasette-cookies-for-magic-parameters]] plugin provides a UI for setting the cookies that populate these parameters.

## Key Characteristics

- Values are populated from the environment, not from user input in the query string.
- Keeps secrets such as API keys out of URLs, where they could otherwise be logged or shared.
- Cookies are the mechanism used by the [[datasette-cookies-for-magic-parameters]] plugin to supply the values.
- A supporting mechanism for the security design of the documentation Q&A experiment, not a central idea of the source post.

## Applications

- Passing an [[OpenAI]] API key to a [[Custom SQL functions|custom SQL function]] in Datasette without exposing the key in query strings.
- Letting a browser user set credentials once through a plugin UI, after which every query that uses the parameter is filled in automatically.

## Related Concepts

- [[concepts/custom-sql-functions|Custom SQL functions]]

## Related Entities

- [[entities/datasette-cookies-for-magic-parameters|datasette-cookies-for-magic-parameters]]
- [[entities/datasette|Datasette]]

## Mentions in Source

- "UI for setting cookies to populate magic parameters" — [[_Inbox/2023-01-15-weeknotes|2023-01-15-weeknotes]]
- "a supporting plugin that helps store secrets such as API keys in cookies so they won’t be transmitted in query strings" — [[_Inbox/2023-01-15-weeknotes|2023-01-15-weeknotes]]