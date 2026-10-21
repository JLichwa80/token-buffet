---
type: concept
created: 2026-10-21
updated: 2026-10-21
tags: [terminology]
aliases:
  - "NDJSON"
  - "--nl option"
sources:
  - "[[sources/2023-08-30-datasette-plus-weeknotes_748a0c]]"

generation_complete: true
---

# newline-delimited JSON

## Definition

Newline-delimited JSON is a format in which each JSON record occupies its own line, rather than all records being wrapped in a single JSON array. Because each line is a complete, independent JSON value, consumers can process records one at a time as they arrive.

## Key Characteristics

- Each line holds one complete JSON record, so no line depends on another to parse.
- Records are not enclosed in a surrounding array, so no opening or closing bracket is needed.
- Output can be streamed and processed incrementally, without loading the full dataset into memory.
- Simple line-oriented tools (such as `grep`, `head`, and `wc -l`) work on the data directly.

## Applications

- **Streaming paginated API output:** [[paginate-json]] writes its results as newline-delimited JSON when run with the `--nl` option, so results can be piped straight into other tools.
- **Loading into a database:** Paired with [[sqlite-utils]] `insert`, newline-delimited JSON lets paginated API data be loaded directly into a SQLite database without an intermediate conversion step.
- **Pipelines:** Each record can be handled as soon as it is fetched, which suits multi-stage command-line pipelines built around [[link pagination]].

## Related Concepts

- [[concepts/link-pagination|link pagination]]

## Related Entities

- [[entities/paginate-json|paginate-json]]
- [[entities/sqlite-utils|sqlite-utils]]

## Mentions in Source

- "The `--nl` option here causes `paginate-json` to output the results as newline-delimited JSON, instead of bundling them together into a JSON array." — [[_Inbox/2023-08-30-datasette-plus-weeknotes|2023-08-30-datasette-plus-weeknotes]]