---
type: entity
created: 2026-10-21
updated: 2026-10-21
generation_complete: true
sources:
  - "[[sources/2023-08-30-datasette-plus-weeknotes_748a0c]]"
  - "[[sources/2023-03-22-weeknotes_1bbf6a]]"
tags:
  - "other"
aliases:
  - "Datasette JSON API pagination"
  - "Datasette JSON API"
---

# Datasette JSON API

## Description

The Datasette JSON API is the machine-readable interface that [[Datasette]] exposes for querying its data. The [[sources/2023-08-30-datasette-plus-weeknotes_748a0c|2023-08-30 weeknotes]] note that it has supported link pagination for some time, so clients can follow next-page links until every row is fetched. Simon Willison uses it with [[paginate-json]], passing `--key rows` to read the array of results from the `"rows"` key. He pipes the newline-delimited output into [[sqlite-utils]] `insert` to load a public PyPI releases dataset into a fresh [[SQLite]] database. The post also presents the [[paginate-json]] 1.0 release, which is the tool that consumes this API.

## Related Entities

- [[entities/datasette|Datasette]]
- [[entities/paginate-json|paginate-json]]
- [[entities/sqlite-utils|sqlite-utils]]
- [[entities/sqlite|SQLite]]

## Related Concepts

- [[concepts/link-pagination|link pagination]]
- [[concepts/newline-delimited-json|newline-delimited JSON]]

## Mentions in Source

- "The [Datasette JSON API](https://docs.datasette.io/en/latest/json_api.html) has supported [link pagination](https://docs.datasette.io/en/latest/json_api.html#pagination) for a while—you can use `paginate-json` with Datasette like this, taking advantage of the new `--key` option to paginate over the array of objects returned in the `"rows"` key:" — [[_Inbox/2023-08-30-datasette-plus-weeknotes|2023-08-30-datasette-plus-weeknotes]]