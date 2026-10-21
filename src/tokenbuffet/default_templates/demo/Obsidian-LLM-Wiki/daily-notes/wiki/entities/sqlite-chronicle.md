---
type: entity
created: 2026-10-21
updated: 2026-10-21
generation_complete: true
sources:
  - "[[sources/2023-12-08-weeknotes_cbd558]]"
  - "[[sources/2023-09-17-weeknotes-embeddings_c2332f]]"
tags:
  - "other"
  - "project"
aliases:
  - "sqlite_chronicle"
---

# sqlite-chronicle

## Description

sqlite-chronicle is an experimental Python library by [[Simon Willison]] that implements a SQL pattern for tracking changes to a SQLite table. It creates a companion chronicle table that triggers on the main table keep up to date, recording when rows were added or updated and whether they were deleted. Change tracking uses a table-wide version number. Willison released sqlite-chronicle 0.2 and 0.2.1 during the reporting period. He plans to use it as the mechanism for persistent enrichments, so that the system can identify which rows still need to be enriched. It is the core library behind [[datasette-chronicle]], which applies the same pattern within Datasette, and it is intended to support [[Datasette Enrichments]].

sqlite-chronicle 0.1 was released on 2023-09-11. It introduced the pattern of using triggers to track when rows in a SQLite table were updated or deleted.

The library is an early SQLite project that relies on triggers rather than a heavier change-capture approach. It is positioned as a lighter-weight alternative to the sqlite-history project. Its design is related to Datasette and sqlite-utils, the tools it is most often discussed alongside.

## Related Entities

- [[entities/datasette-chronicle|datasette-chronicle]]
- [[entities/datasette-enrichments|Datasette Enrichments]]
- [[entities/simon-willison|Simon Willison]]
- [[entities/datasette|Datasette]]
- [[entities/sqlite-utils|sqlite-utils]]

## Related Concepts

- [[concepts/chronicle-table|Chronicle table]]
- [[concepts/rowid|rowid]]

## New Information (2023-09-17-weeknotes-embeddings)

- sqlite-chronicle creates a "chronicle table", a shadow table that records four integer values per row of the main table: added_ms, updated_ms, version and deleted. (This defines the structure of the companion table, which is a defining trait of the library.)
- External processes can store the last version number they saw and then query only the rows inserted or updated since that point. (This describes how consumers use the version number for incremental change detection.)
- sqlite-chronicle is a lighter-weight alternative to the sqlite-history project. (This positions the library relative to a comparable project.)
- Proposed uses include publishing SQLite databases to Datasette with only changed rows sent on each sync, copying tables between databases (including PostgreSQL or MySQL) by copying and deleting only changed rows, saved search alerts that run queries against rows modified since the last run, and showing users "34 rows in this table have changed since your last visit". (These are concrete usage scenarios for the library that the page does not yet list.)

## Mentions in Source

- "`sqlite-chronicle` uses triggers to instead create what I’m calling a “chronicle table”. This is a shadow table that records, for every row in the main table, four integer values:" — [[_Inbox/2023-09-17-weeknotes-embeddings|2023-09-17-weeknotes-embeddings]]
- "`sqlite-chronicle` is a Python library that implements a SQL pattern where a table can have a `_chronicle_tablename` companion table created, which is then updated using triggers against the main table." — [[_Inbox/2023-12-08-weeknotes|2023-12-08-weeknotes]]
- "But... having this table enables some pretty interesting things—because external processes can track the last version number that they saw and use it to see just which rows have been inserted and updated since that point." — [[_Inbox/2023-09-17-weeknotes-embeddings|2023-09-17-weeknotes-embeddings]]
- "That’s a pretty heavy-weight solution. What if there was something lighter that could achieve a lot of the same goals?" — [[_Inbox/2023-09-17-weeknotes-embeddings|2023-09-17-weeknotes-embeddings]]