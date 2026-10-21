---
type: concept
created: 2026-10-21
updated: 2026-10-21
tags: [terminology]
aliases:
  - "Correlated subqueries in SELECT"
  - "Scalar subquery in SELECT list"
sources:
  - "[[sources/2023-02-09-weeknotes_05bd6f]]"

generation_complete: true
---

# Subqueries in select expressions

## Definition

A subquery placed inside the SELECT list of an outer query, so it is evaluated for each output row. In the pattern described for [[SQLite]], the subquery fetches a limited number of related rows for each row returned by the outer query, so a parent row and a bounded set of its children can be retrieved in one query. The technique is comparable to Django's prefetch_related, which solves the same problem.

## Key Characteristics

- Placed in the SELECT list rather than the FROM or WHERE clause.
- Typically correlated: it references columns of the outer row.
- Evaluated once per outer row, so the number of related rows per parent is bounded with a LIMIT inside the subquery.
- Avoids issuing a separate query for each parent row (the N+1 query pattern).
- Makes queries more complex, which is why plan inspection with [[EXPLAIN QUERY PLAN]] is useful when using it.

## Applications

- Retrieving a parent record together with a small, capped list of its related records in a single query, such as a item with its most recent comments.
- Building list or index pages that show a summary of child rows next to each parent row.
- Serving as an in-database alternative to Django's prefetch_related, where the ORM batches related lookups.
- Illustrated in the [[datasette-explain]] demo query, where it shows how queries grow more complex as this pattern is added.

## Related Concepts

- [[concepts/recursive-ctes|Recursive CTEs]]
- [[concepts/explain-query-plan|EXPLAIN QUERY PLAN]]

## Related Entities

- [[entities/sqlite|SQLite]]
- [[entities/datasette-explain|datasette-explain]]

## Mentions in Source

- "This one is a lot more substantial: I wrote up a detailed explanation of a pattern I’ve been exploring in SQLite that lets you fetch back a row AND a limited number of related rows in a single SELECT query." — [[_Inbox/2023-02-09-weeknotes|2023-02-09-weeknotes]]
- "If you’ve ever used Django’s [prefetch\_related](https://docs.djangoproject.com/en/4.1/ref/models/querysets/#prefetch-related) you’ll recognise the problem." — [[_Inbox/2023-02-09-weeknotes|2023-02-09-weeknotes]]