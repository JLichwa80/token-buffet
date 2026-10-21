---
type: entity
created: 2026-10-21
updated: 2026-10-21
tags: [project]
aliases:
  - "SpatiaLite module"
sources:
  - "[[sources/2023-01-15-weeknotes_aefc7f]]"

generation_complete: true
---

# SpatiaLite

## Description

SpatiaLite is a geospatial extension for [[SQLite]]. In the week of 15 January 2023, its SQL functions were found to be able to crash a [[Datasette]] instance, which led to the release of Datasette 0.64 with a `default_allow_sql` setting. The same week, an official Datasette tutorial showed that SpatiaLite can still be used safely to build and deploy a geospatial API that maps locations to time zones. The weeknotes also note that [[shapefile-to-sqlite]] has optional SpatiaLite support for loading shapefiles. SpatiaLite therefore appears both as a security risk and as a practical tool in the week's work.

## Related Entities

- [[entities/datasette|Datasette]]
- [[entities/sqlite|SQLite]]
- [[entities/shapefile-to-sqlite|shapefile-to-sqlite]]

## Related Concepts

- [[concepts/custom-sql-functions|Custom SQL functions]]

## Mentions in Source

- "I released Datasette 0.64 with a new `--setting default_allow_sql off` setting, due to the discovery that some of the SQL functions added by the SpatiaLite module can be used to crash the Datasette instance." — [[_Inbox/2023-01-15-weeknotes|2023-01-15-weeknotes]]
- "It demonstrates how SpatiaLite can be used to safely build and deploy a geospatial API." — [[_Inbox/2023-01-15-weeknotes|2023-01-15-weeknotes]]