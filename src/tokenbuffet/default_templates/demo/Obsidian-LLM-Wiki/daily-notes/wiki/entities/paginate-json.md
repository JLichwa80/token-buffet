---
type: entity
created: 2026-10-21
updated: 2026-10-21
tags: [project]
aliases:
  - "paginate-json 1.0"
sources:
  - "[[sources/2023-08-30-datasette-plus-weeknotes_748a0c]]"

generation_complete: true
---

# paginate-json

## Description

paginate-json is a command-line tool that fetches JSON from paginated APIs by following HTTP link headers. It writes all results either as a single JSON array or, with the `--nl` option, as newline-delimited JSON. Version 1.0 adds several small features and marks the author's confidence in the stability of its design. The tool works with the [[Datasette]] JSON API, which supports [[link pagination]], and it supports the `--key` option for reading rows from a specific key.

## Related Entities

- [[entities/datasette|Datasette]]

## Related Concepts

- [[concepts/link-pagination|link pagination]]

## Mentions in Source

- "My `paginate-json` tool can follow these links for you." — [[_Inbox/2023-08-30-datasette-plus-weeknotes|2023-08-30-datasette-plus-weeknotes]]
- "The 1.0 release adds [a bunch of small features](https://github.com/simonw/paginate-json/releases/tag/1.0), but also marks my confidence in the stability of the design of the tool." — [[_Inbox/2023-08-30-datasette-plus-weeknotes|2023-08-30-datasette-plus-weeknotes]]