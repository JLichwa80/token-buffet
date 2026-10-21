---
type: entity
created: 2026-10-21
updated: 2026-10-21
tags: [project]
aliases:
  - "litecli shell"
sources:
  - "[[sources/2023-08-05-weeknotes-plugins_fc2660]]"

generation_complete: true
---

# litecli

## Description

litecli is a terminal shell for SQLite, written by Amjith Ramanujam, that offers auto-completion against tables and columns. Alex Garcia suggested that the author look at it, and the author then built [[sqlite-utils-litecli]] on top of it. The resulting command opens a full litecli shell that includes all [[Custom SQL functions]] installed by other [[sqlite-utils]] [[Plugins]]. It replaced the author's earlier sqlite-utils-shell plugin as a better alternative.

## Related Entities

- [[entities/sqlite-utils|sqlite-utils]]
- [[entities/datasette|Datasette]]

## Related Concepts

- [[concepts/custom-sql-functions|Custom SQL functions]]
- [[concepts/plugins|Plugins]]

## Mentions in Source

- "Alex Garcia suggested I look at [litecli](https://github.com/dbcli/litecli) by Amjith Ramanujam, which is a much more sophisticated terminal shell for SQLite, incorporating auto-completion against tables and columns." — [[_Inbox/2023-08-05-weeknotes-plugins|2023-08-05-weeknotes-plugins]]