---
type: concept
created: 2026-10-21
updated: 2026-10-21
tags: [terminology]
aliases:
  - "Recursive CTEs"
  - "hierarchical CTEs"
sources:
  - "[[sources/2023-02-09-weeknotes_05bd6f]]"

generation_complete: true
---

# Recursive CTEs

## Definition

A recursive CTE (common table expression) is a SQL common table expression that references itself. It lets a query repeatedly expand a result set, which makes it a way to traverse hierarchical or tree-shaped data within a single statement. In the source, the author uses recursive CTEs in [[SQLite]] to explore hierarchical Twitter threads.

## Key Characteristics

- A CTE that refers to its own name, so each iteration builds on the rows produced by the previous one.
- Suited to tree-shaped data such as threads, parent-child relationships, and hierarchies.
- Supported in [[SQLite]], where the author documented hierarchical CTE patterns in an old Gist before publishing them as a TIL and later as a full article.

## Applications

- Querying hierarchical Twitter threads, where each reply references a parent post (the TIL "Using recursive CTEs to explore hierarchical Twitter threads").
- Walking tree-shaped data stored in relational tables, such as category trees or comment threads.
- Related technique: [[Subqueries in select expressions]] for fetching related rows within a single query.

## Related Concepts

- [[concepts/subqueries-in-select-expressions|Subqueries in select expressions]]

## Related Entities

- [[entities/sqlite|SQLite]]

## Mentions in Source

- "**TIL: [Using recursive CTEs to explore hierarchical Twitter threads](https://til.simonwillison.net/sql/recursive-cte-twitter-threads)**" — [[_Inbox/2023-02-09-weeknotes|2023-02-09-weeknotes]]