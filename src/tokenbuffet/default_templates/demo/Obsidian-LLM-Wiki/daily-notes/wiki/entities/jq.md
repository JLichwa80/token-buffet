---
type: entity
created: 2026-10-21
updated: 2026-10-21
tags: [other]
aliases:
  - "jq language"
  - "jq programs"
sources:
  - "[[sources/2023-08-16-datasette-cloud-weeknotes_9ee111]]"

generation_complete: true
---

# jq

## Description

jq is a command-line JSON processor, and the programs it runs are written in the jq language. In the [[sources/2023-08-16-datasette-cloud-weeknotes_9ee111|2023-08-16 Datasette weeknotes]], it matters because the [[entities/sqlite-utils-jq|sqlite-utils-jq]] plugin exposes it as a SQL function, `jq()`. That function lets users run jq programs against JSON values inside a [[entities/sqlite-utils|sqlite-utils]] SQLite query. The post also shows the same function working inside an interactive litecli shell. This makes jq a building block for querying JSON stored in SQLite.

## Related Entities

- [[entities/sqlite-utils|sqlite-utils]]
- [[entities/sqlite-utils-jq|sqlite-utils-jq]]

## Related Concepts

## Mentions in Source

- "[sqlite-utils-jq](https://github.com/simonw/sqlite-utils-jq) adds a new `jq()` function which can be used to execute [jq](https://jqlang.github.io/jq/) programs as part of a SQL query." — [[_Inbox/2023-08-16-datasette-cloud-weeknotes|2023-08-16-datasette-cloud-weeknotes]]