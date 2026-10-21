---
type: concept
created: 2026-10-21
updated: 2026-10-21
tags: [idea]
aliases:
  - "transform()"
  - "sqlite-utils table transform"
sources:
  - "[[sources/2023-08-30-datasette-plus-weeknotes_748a0c]]"

generation_complete: true
---

# sqlite-utils transform() method

## Definition

The `transform()` method in [[sqlite-utils]] applies schema changes to an existing table by creating a new table with the desired schema, copying the data across, and renaming the new table to replace the original. It superseded the earlier `writable_schema` approach for adding foreign keys, which did not work reliably on some Python installations, such as the system Python on macOS.

## Key Characteristics

- Rebuilds the whole table: creates a new table, copies all rows, then renames it over the original.
- Uses only standard, supported SQLite operations, avoiding direct edits to the schema catalog.
- Slower than the old hack, because every row is copied.
- Handles edge cases that the `writable_schema` approach did not, and works across Python installations.
- The original fast `writable_schema` method was moved into the `sqlite-utils-fast-fks` plugin, so it remains available as an opt-in.

## Applications

- Adding foreign key constraints to an existing SQLite table.
- Changing a table's schema (such as column types or constraints) when a simple `ALTER TABLE` is not sufficient in SQLite.
- Working on a database where speed matters less than reliability across environments.
- Choosing the faster `sqlite-utils-fast-fks` plugin when copying large tables is too slow and the environment supports the older approach.

## Related Concepts

- [[concepts/link-pagination|link pagination]]

## Related Entities

- [[entities/sqlite-utils|sqlite-utils]]
- [[entities/llm|LLM]]

## Mentions in Source

- "That implementation used to work using a deeply gnarly hack: it would switch the `sqlite_master` table over to being writable (using `PRAGMA writable_schema = 1`), update that schema in place to reflect the new foreign keys and then toggle `writable_schema = 0` back again." — [[_Inbox/2023-08-30-datasette-plus-weeknotes|2023-08-30-datasette-plus-weeknotes]]