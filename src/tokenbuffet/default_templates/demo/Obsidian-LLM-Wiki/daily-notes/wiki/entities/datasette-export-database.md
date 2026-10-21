---
type: entity
created: 2026-10-20
updated: 2026-10-20
tags: [other]
aliases:
  - "datasette-export-database plugin"
sources:
  - "[[sources/2024-03-16-weeknotes-the-aftermath-of-nicar_29f231]]"

generation_complete: true
---

# datasette-export-database

## Description

datasette-export-database is a [[Datasette]] plugin, released as version 0.2.1, that exports a snapshot of a SQLite database on demand. It was built because exporting a database that was still accepting writes was previously not safe. The plugin starts a background process that uses [[VACUUM INTO]] to create a temporary file containing a transactional snapshot of the database state, which the user can then download. The post's release section calls it out as a special mention. It is one of several Datasette plugins the author polished for [[Datasette Cloud]].

## Related Entities

- [[entities/datasette|Datasette]]
- [[entities/datasette-cloud|Datasette Cloud]]

## Related Concepts

- [[concepts/vacuum-into|VACUUM INTO]]

## Mentions in Source

- "[datasette-export-database](https://datasette.io/plugins/datasette-export-database) provides a way to export a current snapshot of a SQLite database from Datasette—something that previously wasn’t safe to do for databases that were accepting writes." — [[_Inbox/2024-03-16-weeknotes-the-aftermath-of-nicar|2024-03-16-weeknotes-the-aftermath-of-nicar]]