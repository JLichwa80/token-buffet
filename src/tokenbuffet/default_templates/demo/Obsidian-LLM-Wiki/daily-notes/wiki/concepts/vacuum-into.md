---
type: concept
created: 2026-10-20
updated: 2026-10-20
tags: [terminology]
aliases:
  - "SQLite VACUUM INTO"
sources:
  - "[[sources/2024-03-16-weeknotes-the-aftermath-of-nicar_29f231]]"

generation_complete: true
---

# VACUUM INTO

## Definition

VACUUM INTO is a SQLite command that writes a transactionally consistent copy of a database to a new file. Because the copy is taken within a transaction, it is a safe snapshot even when the source database is still accepting writes.

## Key Characteristics

- Writes a full copy of a SQLite database to a new file rather than modifying the source.
- Produces a transactionally consistent snapshot, even while other connections are writing.
- Creates a temporary file that can then be served or downloaded.
- Used as the underlying mechanism for [[datasette-export-database|datasette-export-database]] to make consistent exports.

## Applications

- Making safe, consistent exports of live SQLite databases served by [[Datasette]].
- Enabling a download of a database through an [[action buttons|action button]] without risking a corrupt or inconsistent copy.
- Previously, exporting a database that was still accepting writes was not safe in Datasette; VACUUM INTO removes that risk.

## Related Concepts

- [[concepts/action-buttons|action buttons]]

## Related Entities

- [[entities/datasette-export-database|datasette-export-database]]
- [[entities/datasette|Datasette]]

## Mentions in Source

- "It works by kicking off a background process to use `VACUUM INTO` in SQLite to create a temporary file with a transactional snapshot of the database state, then lets the user download that file." — [[_Inbox/2024-03-16-weeknotes-the-aftermath-of-nicar|2024-03-16-weeknotes-the-aftermath-of-nicar]]