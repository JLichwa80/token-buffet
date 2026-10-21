---
type: entity
created: 2026-10-21
updated: 2026-10-21
generation_complete: true
sources:
  - "[[sources/2023-08-30-datasette-plus-weeknotes_748a0c]]"
  - "[[sources/2023-05-01-weeknotes_72fe7e]]"
  - "[[sources/2023-04-23-weeknotes_572e37]]"
  - "[[sources/2023-03-22-weeknotes_1bbf6a]]"
  - "[[sources/2023-02-09-weeknotes_05bd6f]]"
  - "[[sources/2023-01-15-weeknotes_aefc7f]]"
tags:
  - "other"
  - "project"
aliases:
  - "SQLite database"
  - "sqlite3"
---

# SQLite

## Description

SQLite is an embedded SQL database engine that [[Datasette]], [[sqlite-utils]], and [[LLM]] all rely on for storage. A known limitation is that SQLite does not support adding foreign keys to an existing table out of the box. Earlier, [[sqlite-utils]] worked around this by directly editing the `sqlite_master` schema table, a hack that broke on some [[Python]] installations. Simon Willison replaced that hack with the [[sqlite-utils transform() method|transform() method]], which rebuilds the table, and moved the old fast method into the sqlite-utils-fast-fks plugin. This SQLite behavior is the reason the foreign-key change was necessary.

Until recently, the TIL site's social media card images were stored as PNG files directly in a SQLite database. When the database grew past Vercel's 50MB deployment size limit, the images were moved out of SQLite and into an S3 bucket. Separately, openai-to-sqlite 0.3 added a custom SQL function that calls the chatgpt() API, so SQL queries can update existing SQLite tables in place with the results, such as sentiment analysis. This shows SQLite being extended with custom SQL functions that enrich data where it sits, a pattern common across the Datasette ecosystem.

Simon Willison first wrote up hierarchical recursive CTEs in SQLite in an old Gist, long before his TIL site, and later expanded that work into a full article. This adds recursive CTEs to the list of SQLite capabilities used for hierarchical data.

SQLite also supports subqueries in select expressions, which let a single SELECT fetch a row together with a limited number of related rows, similar to Django's `prefetch_related`. The page does not yet cover this technique.

Several releases from the same week store their data in SQLite, including openai-to-sqlite, which saves OpenAI API responses to a SQLite database for later use such as calculating embeddings, and shapefile-to-sqlite, which loads geographic shapefiles into SQLite, optionally with SpatiaLite, an extension that adds geospatial features to SQLite. Datasette 0.64 added a `--setting default_allow_sql off` option after some SQL functions added by the SpatiaLite module were found to be able to crash a Datasette instance, which shows the risk of loading custom SQL functions into SQLite. A TIL post also covers Geopoly, SQLite's feature for geographic polygon operations.
## Related Entities

- [[entities/sqlite-utils|sqlite-utils]]
- [[entities/llm|LLM]]
- [[entities/python|Python]]
- [[entities/datasette|Datasette]]

## Related Concepts

- [[concepts/foreign-keys|foreign keys]]
- [[concepts/sqlite-utils-transform-method|sqlite-utils transform() method]]

## New Information (2023-02-09-weeknotes)

- SQLite's select datetime('now') returns a value that stays stable within the same query. (This is a defining behavior of SQLite's datetime function that fits the page's characteristics list.)
- The EXPLAIN QUERY PLAN output that datasette-explain shows is produced by SQLite. (It documents a SQLite feature (query plan explanation) that Datasette tooling exposes, which the page does not currently mention.)

## Mentions in Source

- "This TIL is actually a learned-several-years-ago: I wrote up notes on hierarchical CTEs in SQLite in [an old Gist](https://gist.github.com/simonw/656a8c6e4688f720773c474080abe1b0), long before I started my TIL website." — [[_Inbox/2023-02-09-weeknotes|2023-02-09-weeknotes]]
- "Not much to say about this one: it relates to `select datetime('now')` in SQLite." — [[_Inbox/2023-02-09-weeknotes|2023-02-09-weeknotes]]
- "Until recently it stored these images as PNG files directly in the SQLite database itself." — [[_Inbox/2023-05-01-weeknotes|2023-05-01-weeknotes]]
- "To fix it, I moved the images out of the SQLite database and put them in an S3 bucket instead." — [[_Inbox/2023-05-01-weeknotes|2023-05-01-weeknotes]]
- "`sqlite-utils` has a mechanism for adding foreign keys to an existing table—something that’s not supported by SQLite out of the box." — [[_Inbox/2023-08-30-datasette-plus-weeknotes|2023-08-30-datasette-plus-weeknotes]]
- "Load shapefiles into a SQLite (optionally SpatiaLite) database" — [[_Inbox/2023-01-15-weeknotes|2023-01-15-weeknotes]]
- "a command-line tool for storing OpenAI API responses in a SQLite database—useful for calculating embeddings" — [[_Inbox/2023-01-15-weeknotes|2023-01-15-weeknotes]]