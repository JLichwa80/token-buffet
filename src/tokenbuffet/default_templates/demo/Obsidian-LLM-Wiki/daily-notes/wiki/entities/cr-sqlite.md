---
type: entity
created: 2026-10-21
updated: 2026-10-21
tags: [project]
aliases:
  - "cr-sqlite extension"
sources:
  - "[[sources/2023-09-17-weeknotes-embeddings_c2332f]]"

generation_complete: true
---

# cr-sqlite

## Description

cr-sqlite is an extension that adds full [[CRDT|CRDT]] support to [[SQLite]]. It is intended to let multiple databases accept writes independently and then merge them automatically, without manual conflict resolution. [[2023-09-17-weeknotes-embeddings|Simon Willison]] tried cr-sqlite on macOS and published a TIL about it on 2023-09-13, which he links from his 2023-09-17 weeknotes. He describes the capability as "a very exciting capability". The extension is the concrete example in this source of the CRDT approach, which is the main concept the source introduces for syncing SQLite data.

## Related Entities

- [[entities/sqlite-utils|sqlite-utils]]

## Related Concepts

- [[concepts/crdt|CRDT]]

## Mentions in Source

- "cr-sqlite adds full CRDTs to SQLite, which should enable multiple databases to accept writes independently and then seamlessly merge them together." — [[_Inbox/2023-09-17-weeknotes-embeddings|2023-09-17-weeknotes-embeddings]]