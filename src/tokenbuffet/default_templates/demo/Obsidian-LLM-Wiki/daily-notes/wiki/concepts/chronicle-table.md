---
type: concept
created: 2026-10-21
updated: 2026-10-21
generation_complete: true
sources:
  - "[[sources/2023-12-08-weeknotes_cbd558]]"
  - "[[sources/2023-09-17-weeknotes-embeddings_c2332f]]"
tags:
  - "terminology"
  - "idea"
aliases:
  - "_chronicle_tablename"
  - "chronicle tracking table"
---

# Chronicle table

## Definition

A chronicle table is the companion table that [[sqlite-chronicle]] creates for a tracked SQLite table. It holds one shadow row for each row in the main table, keyed by the same primary keys. Its columns record when each row was last inserted or updated, using a table-wide version counter. Triggers on the main table keep it synchronized.

## Key Characteristics

- Has the same primary keys as the main table, with one shadow row per tracked row.
- Stores `added_ms` and `updated_ms` as millisecond timestamps.
- Stores an integer `version` column that is drawn from a table-wide counter.
- Stores a boolean `deleted` indicator.
- Is kept current by triggers defined on the main table.
- Chronicle tables are a lighter alternative to the full-copy approach used by sqlite-history, storing metadata about changes rather than complete copies of each row.
- Chronicle tables are keyed by primary keys rather than SQLite rowid, because rowid values are unstable and change on VACUUM.
## Applications

- Change tracking: finding rows inserted or updated after a given point, by filtering on `version` or the timestamps.
- Synchronization: letting an external consumer pull only the rows that changed since its last sync.
- Soft-delete awareness: using the `deleted` indicator to distinguish removed rows from live ones.
- Tooling integration: [[datasette-chronicle]] relies on chronicle tables to expose change history in Datasette.
- Table copying: copying tables to other databases, which Willison proposes as a use of chronicle tables.
- Saved search alerts: sending alerts for saved searches, which Willison proposes as a use of chronicle tables.
## Related Concepts

## Related Entities

- [[entities/sqlite-chronicle|sqlite-chronicle]]
- [[entities/datasette-chronicle|datasette-chronicle]]

## Mentions in Source

- "The chronicle table has a shadow row for every row in the main table, duplicating its primary keys and then storing millisecond timestamp columns for `added_ms` and `updated_ms`, an integer `version` column and a `deleted` boolean indicator." — [[_Inbox/2023-12-08-weeknotes|2023-12-08-weeknotes]]
- "`sqlite-chronicle` uses triggers to instead create what I’m calling a “chronicle table”. This is a shadow table that records, for every row in the main table, four integer values:" — [[_Inbox/2023-09-17-weeknotes-embeddings|2023-09-17-weeknotes-embeddings]]
- "Publishing SQLite databases up to Datasette, sending only the rows that have changed since the last sync." — [[_Inbox/2023-09-17-weeknotes-embeddings|2023-09-17-weeknotes-embeddings]]