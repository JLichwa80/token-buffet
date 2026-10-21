---
type: entity
created: 2026-10-21
updated: 2026-10-21
tags: [other]
aliases:
  - "Datasette Chronicle"
sources:
  - "[[sources/2023-12-08-weeknotes_cbd558]]"

generation_complete: true
---

# datasette-chronicle

## Description

datasette-chronicle is a Datasette plugin that exposes [[sqlite-chronicle]] change tracking inside Datasette. It adds "enable/disable chronicle tracking" table actions for users with the correct permissions, which turn tracking on or off for a specific table in the Datasette UI. For tables with tracking enabled, it provides a `?_since=VERSION` query string parameter that filters the table to rows changed since the given version. Simon Willison released version 0.2 on 2023-12-06, as recorded in [[sources/2023-12-08-weeknotes_cbd558]]. It is the Datasette-facing layer of the change-tracking work Willison built on [[sqlite-chronicle]], and he planned to use it for persistent [[Datasette Enrichments]].

## Related Entities

- [[entities/sqlite-chronicle|sqlite-chronicle]]
- [[entities/datasette-enrichments|Datasette Enrichments]]
- [[entities/simon-willison|Simon Willison]]
- [[entities/datasette-cloud|Datasette Cloud]]

## Related Concepts

- [[concepts/chronicle-table|Chronicle table]]

## Mentions in Source

- "I also started a new plugin to accompany the feature: [datasette-chronicle](https://datasette.io/plugins/datasette-chronicle), which adds two features to Datasette:" — [[_Inbox/2023-12-08-weeknotes|2023-12-08-weeknotes]]
- "For tables that have chronicle enabled, a `?_since=VERSION` querystring parameter which can be used to filter the table to only rows that have changed since the specified version" — [[_Inbox/2023-12-08-weeknotes|2023-12-08-weeknotes]]