---
type: concept
created: 2026-10-21
updated: 2026-10-21
tags: [idea]
aliases:
  - "live SQL error checking"
sources:
  - "[[sources/2023-02-09-weeknotes_05bd6f]]"

generation_complete: true
---

# live error checking

## Definition

Live error checking is the idea of validating a SQL query as the user types it and showing any errors immediately.

## Key Characteristics

- Runs validation on each edit, so errors appear while the query is still being written.
- Depends on [[EXPLAIN QUERY PLAN]] being fast enough to run on every keystroke.
- Is the part of [[datasette-explain]] the author likes most, ahead of its explain output and column listings.
- Is a candidate for inclusion in [[Datasette]] core, according to the author.
- Is distinct from live result previews, which the author is less sure about.

## Applications

- Catching syntax and schema errors in a SQL editor before the query is run.
- Giving feedback in a web-based query interface such as [[Datasette]] as the user types.

## Related Concepts

- [[concepts/explain-query-plan|EXPLAIN QUERY PLAN]]

## Related Entities

- [[entities/datasette-explain|datasette-explain]]
- [[entities/datasette|Datasette]]

## Mentions in Source

- "I really like the error checking mode—much more so than the explain output and table and columns." — [[_Inbox/2023-02-09-weeknotes|2023-02-09-weeknotes]]
- "I’m tempted to bring live error checking like this to Datasette core." — [[_Inbox/2023-02-09-weeknotes|2023-02-09-weeknotes]]