---
type: concept
created: 2026-10-21
updated: 2026-10-21
tags: [terminology]
aliases:
  - "SQLite row identifier"
sources:
  - "[[sources/2023-09-17-weeknotes-embeddings_c2332f]]"

generation_complete: true
---

# rowid

## Definition

In [[SQLite]], `rowid` is an internal integer identifier that every table row has. Its value is managed by SQLite rather than the application, and it is not guaranteed to stay the same over the life of a row.

## Key Characteristics

- An internal integer key assigned to each table row by SQLite.
- Not a stable identifier: values can be rewritten when a table is rebuilt, such as by `table.transform()` in [[sqlite-utils]].
- Values are also rewritten when a database is `VACUUM`ed, so a `rowid` read before a VACUUM may not match one read after it.
- Applications that treat `rowid` as a permanent key can break silently, as with [[full-text search]] indexes that point at rows by `rowid`.

## Applications

- **Data-integrity lesson**: Willison's experience with `sqlite-utils` showed that a `rowid` rewrite can break full-text search on [[Datasette Cloud]].
- **Feature design in Datasette**: After learning `rowid` is unstable, Willison decided that future [[Datasette]] features should not assume it is a stable identifier.
- **Row comments**: He suggests that features such as row comments need tables with a proper foreign key, not a `rowid` reference.
- **Change tracking**: The instability motivated [[chronicle table]] designs, which let external systems sync only changed rows without relying on `rowid`.

## Related Concepts

- [[concepts/chronicle-table|chronicle table]]
- [[concepts/database-backed-access-tokens|database-backed access tokens]]

## Related Entities

- [[entities/sqlite-utils|sqlite-utils]]
- [[entities/datasette|Datasette]]
- [[entities/datasette-cloud|Datasette Cloud]]

## Mentions in Source

- "But then... I learned that `rowid` in SQLite has always been unstable—they are rewritten any time someone VACUUMs a table!" — [[_Inbox/2023-09-17-weeknotes-embeddings|2023-09-17-weeknotes-embeddings]]
- "I’ve been designing future features for Datasette that assume that `rowid` is a useful stable identifier for a row." — [[_Inbox/2023-09-17-weeknotes-embeddings|2023-09-17-weeknotes-embeddings]]