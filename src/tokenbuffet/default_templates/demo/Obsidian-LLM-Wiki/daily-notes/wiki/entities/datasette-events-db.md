---
type: entity
created: 2026-10-21
updated: 2026-10-21
tags: [project]
aliases:
  - "datasette-events-db 0.1a0"
sources:
  - "[[sources/2024-02-09-weeknotes_1bab97]]"

generation_complete: true
---

# datasette-events-db

## Description

datasette-events-db is a [[Datasette]] plugin released as version 0.1a0 on 8 February 2024. It hooks into the event tracking mechanism introduced in Datasette 1.0a8 and logs events such as create-table and login to a `datasette_events` table. The author released it partly as a debugging tool and partly to make sure each Datasette plugin hook has at least one released plugin that uses it. It is a concrete example of the author's approach to exercising Datasette's plugin API.

## Related Entities

- [[entities/datasette|Datasette]]

## Related Concepts

## Mentions in Source

- "**[datasette-events-db](https://datasette.io/plugins/datasette-events-db)** hooks into the new [events mechanism](https://docs.datasette.io/en/1.0a8/plugin_hooks.html#event-tracking) in Datasette 1.0a8 and logs any events (`create-table`, `login` etc) to a `datasette_events` table." — [[_Inbox/2024-02-09-weeknotes|2024-02-09-weeknotes]]