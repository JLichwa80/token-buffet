---
type: entity
created: 2026-10-21
updated: 2026-10-21
generation_complete: true
sources:
  - "[[sources/2023-10-30-weeknotes_d4a215]]"
  - "[[sources/2023-09-17-weeknotes-embeddings_c2332f]]"
tags:
  - "other"
  - "project"
aliases:
  - "sqlite-migrate plugin"
---

# sqlite-migrate

## Description

sqlite-migrate is a plugin for [[sqlite-utils]] that adds a simple migration system for applying changes to a database schema in a controlled, repeatable way. Version 0.1b0 fixed a bug, reported by Alex Garcia, in which overlapping migration names across multiple migration sets were handled incorrectly. The fix changed the schema of the `_sqlite_migrations` table, and the author applied it with a conditional check. The author argues that sqlite-migrate combined with sqlite-utils' `table.transform()` method is a robust answer to SQLite migration difficulties.

sqlite-migrate was first released as version 0.1a2 on 2023-09-03, described as a simple database migration system for SQLite built on [[sqlite-utils]]. It was inspired by Django migrations, with a less sophisticated feature set, and at 0.1a2 it was still marked alpha, with the author saying it would soon move to non-alpha status. The author used sqlite-migrate in [[llm]] to manage the schema for storing embeddings, and it was beginning to appear in some Datasette plugins.

The 2023-09-17 weeknotes ("2023-09-17-weeknotes-embeddings") confirm this status: sqlite-migrate was still alpha, the author was using it in [[llm]] to manage the schema that stores embeddings, and it was beginning to show up in some Datasette plugins.

## Related Entities

- [[entities/datasette-edit-schema|datasette-edit-schema]]
- [[entities/llm|LLM]]
- [[entities/sqlite-utils|sqlite-utils]]

## Related Concepts

- [[concepts/embeddings|Embeddings]]

## Mentions in Source

- "I’m using it in LLM now to manage the schema used to store embeddings, and it’s beginning to show up in some Datasette plugins as well." — [[_Inbox/2023-09-17-weeknotes-embeddings|2023-09-17-weeknotes-embeddings]]
- "[sqlite-migrate](https://github.com/simonw/sqlite-migrate) is my plugin that adds a simple migration system to [sqlite-utils](https://sqlite-utils.datasette.io/), for applying changes to a database schema in a controlled, repeatable way." — [[_Inbox/2023-10-30-weeknotes|2023-10-30-weeknotes]]