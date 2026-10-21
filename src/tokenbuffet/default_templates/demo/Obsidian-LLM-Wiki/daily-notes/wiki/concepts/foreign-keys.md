---
type: concept
created: 2026-10-21
updated: 2026-10-21
tags: [terminology]
aliases:
  - "SQLite foreign keys"
  - "FK"
sources:
  - "[[sources/2023-08-30-datasette-plus-weeknotes_748a0c]]"

generation_complete: true
---

# foreign keys

## Definition

A foreign key is a constraint that links a column in one table to a column in another table, so that values in the first column must correspond to existing values in the second.

## Key Characteristics

- Links a column in one table to a column in another table.
- SQLite does not support adding a foreign key to an existing table out of the box.
- Before sqlite-utils 3.35, adding them relied on a fragile hack that edited the `sqlite_master` schema table directly.
- Since sqlite-utils 3.35, foreign keys are added through the [[sqlite-utils transform() method]], which copies the table into a new one with the constraint.
- The removed hack's behaviour is preserved in the [[sqlite-utils-fast-fks]] plugin.

## Applications

- Adding foreign key constraints to existing SQLite tables with [[sqlite-utils]], using `transform()` rather than direct schema edits.
- Using [[sqlite-utils-fast-fks]] to retain the original direct-schema-edit approach for adding foreign keys to existing tables.

## Related Concepts

- [[concepts/sqlite-utils-transform-method|sqlite-utils transform() method]]

## Related Entities

- [[entities/sqlite-utils|sqlite-utils]]
- [[entities/sqlite-utils-fast-fks|sqlite-utils-fast-fks]]

## Mentions in Source

- "`sqlite-utils` has a mechanism for adding foreign keys to an existing table—something that’s not supported by SQLite out of the box." — [[_Inbox/2023-08-30-datasette-plus-weeknotes|2023-08-30-datasette-plus-weeknotes]]