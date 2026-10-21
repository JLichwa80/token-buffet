---
type: entity
created: 2026-10-21
updated: 2026-10-21
generation_complete: true
sources:
  - "[[sources/2024-02-27-weeknotes-getting-ready-for-nicar_823782]]"
  - "[[sources/2023-10-30-weeknotes_d4a215]]"
  - "[[sources/2023-09-17-weeknotes-embeddings_c2332f]]"
tags:
  - "project"
  - "other"
aliases:
  - "Datasette Edit Schema plugin"
---

# datasette-edit-schema

## Description

datasette-edit-schema is a [[Datasette]] plugin for modifying table schemas. Version 0.8a0 was released on 2024-02-18 and added fine-grained permission support. The plugin now respects Datasette's core `create-table`, `alter-table` and `drop-table` permissions. The `alter-table` permission was introduced in Datasette 1.0a9, released two weeks before this release. Simon Willison describes the release as "a pretty significant release" in the [[Datasette]] weeknotes of 2024-02-27.

datasette-edit-schema 0.7, released on 2023-10-26, added the ability to add and remove indexes on larger tables, which speeds up faceting. The feature came from feedback on the Datasette Cloud preview. The 2023-10-30 weeknotes record the same request and name 0.7 as the release that adds it. The plugin's README screenshot is updated automatically by a script, `update-screenshot.sh`, which uses shot-scraper.

datasette-edit-schema 0.6 was a major release, announced in the [[2023-09-17-weeknotes-embeddings]] weeknotes, that added three significant features: creating new tables, editing primary keys, and modifying foreign key constraints. At its core, the [[Datasette]] plugin lets users edit table schemas, including adding and removing columns, changing column types and reordering columns. Willison released 0.6 because these schema tools complement the row editing UI in [[entities/datasette-write-ui|datasette-write-ui]]. The foreign key support matters because it makes Datasette's API more useful for following relationships between tables.

## Related Entities

- [[entities/datasette|Datasette]]
- [[entities/datasette-cloud|Datasette Cloud]]
- [[entities/sqlite-migrate|sqlite-migrate]]
- [[entities/datasette-write-ui|datasette-write-ui]]

## Related Concepts

- [[concepts/foreign-key-constraints|Foreign key constraints]]

## Mentions in Source

- "datasette-edit-schema 0.6 is a major release, with three significant new features:" — [[_Inbox/2023-09-17-weeknotes-embeddings|2023-09-17-weeknotes-embeddings]]
- "We’re iterating on Datasette Cloud based on feedback from people using the preview. One request was the ability to add and remove indexes from larger tables, to help speed up faceting." — [[_Inbox/2023-10-30-weeknotes|2023-10-30-weeknotes]]
- "[datasette-edit-schema 0.7](https://github.com/simonw/datasette-edit-schema/releases/tag/0.7) adds that feature." — [[_Inbox/2023-10-30-weeknotes|2023-10-30-weeknotes]]
- "This is a pretty significant release: it adds finely-grained permission support such that Datasette’s core `create-table`, `alter-table` and `drop-table` permissions are now respected by the plugin." — [[_Inbox/2024-02-27-weeknotes-getting-ready-for-nicar|2024-02-27-weeknotes-getting-ready-for-nicar]]