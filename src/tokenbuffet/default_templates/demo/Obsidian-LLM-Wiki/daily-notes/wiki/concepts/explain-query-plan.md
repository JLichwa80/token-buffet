---
type: concept
created: 2026-10-21
updated: 2026-10-21
tags: [terminology]
aliases:
  - "query plan"
sources:
  - "[[sources/2023-02-09-weeknotes_05bd6f]]"

generation_complete: true
---

# EXPLAIN QUERY PLAN

## Definition

EXPLAIN QUERY PLAN is an SQLite command that reports how the database engine intends to execute a given query. It is the core mechanism behind [[datasette-explain]], which runs it on query text as the user types and displays either the output or any error message.

## Key Characteristics

- Provided by [[SQLite]]; it describes the planned execution strategy without running the query.
- Fast enough to run on every keystroke, even for complex queries, according to the author of [[datasette-explain]].
- Returns either a plan or an error, which makes it usable for [[live error checking]].
- Shows which tables a query references, so it can help identify the tables involved.

## Applications

- **Live query feedback:** [[datasette-explain]] runs EXPLAIN QUERY PLAN while the user types and shows the result or error message.
- **Error detection while typing:** Because the command is quick, syntax and reference errors surface immediately rather than on submission.
- **Table discovery:** The plan output identifies which tables a query touches, which helps users understand unfamiliar queries.
- **Query inspection:** Users can check how the engine intends to run a query before executing it, including nested queries such as [[Subqueries in select expressions]].

## Related Concepts

- [[concepts/live-error-checking|live error checking]]
- [[concepts/subqueries-in-select-expressions|Subqueries in select expressions]]

## Related Entities

- [[entities/datasette-explain|datasette-explain]]
- [[entities/sqlite|SQLite]]

## Mentions in Source

- "It runs `explain query plan ...` on the query you have typed so far. If this returns an error message (because the query isn’t complete or includes problems) that message is displayed to the end user." — [[_Inbox/2023-02-09-weeknotes|2023-02-09-weeknotes]]
- "It’s worth highlighting that the queries themselves are *really* fast—no matter how complex the SQL query, running `explain query plan ...` against it is very quick." — [[_Inbox/2023-02-09-weeknotes|2023-02-09-weeknotes]]