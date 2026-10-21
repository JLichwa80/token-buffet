---
type: entity
created: 2026-10-21
updated: 2026-10-21
tags: [project]
aliases:
  - "OpenCage enrichment plugin"
sources:
  - "[[sources/2024-02-27-weeknotes-getting-ready-for-nicar_823782]]"

generation_complete: true
---

# datasette-enrichments-opencage

## Description

datasette-enrichments-opencage is a [[Datasette]] plugin that provides geocoding and reverse geocoding using the OpenCage service. Version 0.1.1 was released on 2024-02-16 to fix a "database locked" error that occurred occasionally in [[Datasette Cloud]]. The bug came from the plugin running write operations without short, well-defined transactions. Simon Willison's fix made the plugin wrap its writes correctly, and the bug led him to change [[Datasette]] core in release 1.0a10, which now automatically wraps `database.execute_write_fn()` calls in a transaction. The plugin is one of the enrichment plugins in the wider [[Datasette Enrichments]] family.

## Related Entities

- [[entities/datasette-cloud|Datasette Cloud]]
- [[entities/datasette|Datasette]]
- [[entities/datasette-enrichments|Datasette Enrichments]]

## Related Concepts

## Mentions in Source

- "> * **[datasette-enrichments-opencage 0.1.1](https://github.com/datasette/datasette-enrichments-opencage/releases/tag/0.1.1)**—2024-02-16  
>   Geocoding and reverse geocoding using OpenCage" — [[_Inbox/2024-02-27-weeknotes-getting-ready-for-nicar|2024-02-27-weeknotes-getting-ready-for-nicar]]
- "This resolves a dreaded “database locked” error I was seeing occasionally in Datasette Cloud." — [[_Inbox/2024-02-27-weeknotes-getting-ready-for-nicar|2024-02-27-weeknotes-getting-ready-for-nicar]]