---
type: entity
created: 2026-10-21
updated: 2026-10-21
tags: [project]
aliases:
  - "datasette-explain 0.1a0"
sources:
  - "[[sources/2023-02-09-weeknotes_05bd6f]]"

generation_complete: true
---

# datasette-explain

## Description

datasette-explain is a [[Datasette]] plugin released as version 0.1a0 on 2023-02-09, and it is the main feature of the post in which it was announced. It adds a feature to the Datasette SQL query editing page that continuously runs [[EXPLAIN QUERY PLAN]] on the query as the user types and displays the results. The typed SQL is sent in the background to a `/db/-/explain` endpoint, which returns either the error message or the query plan. When the query is valid, the plugin also lists the tables referenced in the query and their columns to help the user while typing. The author describes the plugin as very much an alpha and says its error checking mode, known as [[live error checking]], is the most useful part.

## Related Entities

- [[entities/datasette|Datasette]]
- [[entities/sqlite|SQLite]]

## Related Concepts

- [[concepts/explain-query-plan|EXPLAIN QUERY PLAN]]
- [[concepts/live-error-checking|live error checking]]
- [[concepts/subqueries-in-select-expressions|Subqueries in select expressions]]

## Mentions in Source

- "Just one new plugin this week: [datasette-explain](https://github.com/simonw/datasette-explain), which adds a feature to the Datasette SQL query editing page which constantly runs `explain query plan ...` on the query you’re typing and shows the results." — [[_Inbox/2023-02-09-weeknotes|2023-02-09-weeknotes]]
- "The plugin works by sending the SQL query you have typed to a `/db/-/explain` endpoint in the background." — [[_Inbox/2023-02-09-weeknotes|2023-02-09-weeknotes]]