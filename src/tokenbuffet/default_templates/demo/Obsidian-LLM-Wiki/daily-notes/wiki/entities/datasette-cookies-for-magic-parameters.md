---
type: entity
created: 2026-10-21
updated: 2026-10-21
tags: [other]
aliases:
  - "magic parameters cookies plugin"
sources:
  - "[[sources/2023-01-15-weeknotes_aefc7f]]"

generation_complete: true
---

# datasette-cookies-for-magic-parameters

## Description

datasette-cookies-for-magic-parameters is a supporting [[Datasette]] plugin that stores secrets, such as API keys, in cookies. Keeping secrets in cookies keeps them out of URL query strings, where they could otherwise be transmitted or logged. The plugin was released as version 0.1.2 on 12 January 2023. It provides a UI for setting the cookies that populate [[Magic parameters]]. It supports the Q&A experiment by making [[openai]] credentials easier to handle safely, and it is one of the four software releases tied to the documentation Q&A work.

## Related Entities

- [[entities/datasette|Datasette]]
- [[entities/openai|openai]]

## Related Concepts

- [[concepts/magic-parameters|Magic parameters]]

## Mentions in Source

- "[datasette-cookies-for-magic-parameters](https://datasette.io/plugins/datasette-cookies-for-magic-parameters)—a supporting plugin that helps store secrets such as API keys in cookies so they won’t be transmitted in query strings" — [[_Inbox/2023-01-15-weeknotes|2023-01-15-weeknotes]]