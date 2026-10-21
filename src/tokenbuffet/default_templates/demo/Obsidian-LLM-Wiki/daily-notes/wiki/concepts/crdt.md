---
type: concept
created: 2026-10-21
sources:
  - "[[sources/2023-09-17-weeknotes-embeddings_c2332f]]"
tags: [terminology]
stub: true
generation_complete: true
---
# CRDT

> Stub created by the ingest candidate gate (prose+named) — [[sources/2023-09-17-weeknotes-embeddings_c2332f]] names this without treating it. Will be filled by the next ingest of a source that does.

CRDT stands for conflict-free replicated data type, a structure that lets multiple replicas accept writes independently and merge them without conflicts. Willison highlights cr-sqlite, which adds CRDTs to SQLite so that separate databases can merge their writes seamlessly. He tried it on macOS in a TIL. The concept is relevant to the post's wider interest in synchronizing SQLite data across systems.

> "[cr-sqlite](https://github.com/vlcn-io/cr-sqlite) adds full CRDTs to SQLite, which should enable multiple databases to accept writes independently and then seamlessly merge them together." — [[sources/2023-09-17-weeknotes-embeddings_c2332f]]
