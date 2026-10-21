---
type: concept
created: 2026-10-21
updated: 2026-10-21
tags: [terminology]
aliases:
  - "SQLite ALTER TABLE"
  - "ALTER TABLE statement"
sources:
  - "[[sources/2023-10-30-weeknotes_d4a215]]"

generation_complete: true
---

# ALTER TABLE

## Definition

ALTER TABLE is the SQL statement used to change the structure of an existing table, such as its columns. In SQLite, its core implementation supports only a limited set of changes, which makes schema migrations difficult. Tools such as [[sqlite-migrate]] and the `table.transform()` method in [[sqlite-utils]] provide workarounds for these constraints.

## Key Characteristics

- Modifies the structure of an existing table rather than its data.
- SQLite's core implementation supports a restricted set of structural changes.
- Limited support makes multi-step schema migrations harder to perform directly.
- Workarounds typically rebuild the table (create a new table, copy data, and swap it in) rather than altering it in place.

## Applications

- Changing an existing table's columns during a schema migration in SQLite.
- Running schema changes through [[sqlite-migrate]], which manages migrations in SQLite databases.
- Applying structural changes with the `table.transform()` method in [[sqlite-utils]], which works around SQLite's ALTER TABLE limits.

## Related Concepts

## Related Entities

- [[entities/sqlite-utils|sqlite-utils]]
- [[entities/sqlite-migrate|sqlite-migrate]]

## Mentions in Source

- "A [recent thread about SQLite](https://news.ycombinator.com/item?id=38036921) on Hacker News included a surprising number of complaints about the difficulty of running migrations, due to the lack of features of the core `ALTER TABLE` implementation." — [[_Inbox/2023-10-30-weeknotes|2023-10-30-weeknotes]]