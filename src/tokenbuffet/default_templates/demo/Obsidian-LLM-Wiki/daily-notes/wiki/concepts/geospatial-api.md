---
type: concept
created: 2026-10-21
updated: 2026-10-21
tags: [terminology]
aliases:
  - "Location to Time Zone API"
  - "Geospatial Web API"
sources:
  - "[[sources/2023-01-15-weeknotes_aefc7f]]"

generation_complete: true
---

# Geospatial API

## Definition

A geospatial API is a web API that answers location-based queries, such as mapping a latitude and longitude to a time zone. The source presents a geospatial API built with [[SpatiaLite]] as the subject of the latest official [[Datasette]] tutorial, showing that spatial SQL extensions can power a public-facing API built on Datasette.

## Key Characteristics

- Accepts location inputs (for example, latitude and longitude) and returns spatial results.
- Relies on spatial SQL functions, here provided by [[SpatiaLite]], to compute answers.
- Is exposed over the web and can be deployed for public use.
- Must be secured against unsafe SQL execution. The source's [[SpatiaLite]] SQL function crash warning led to the `default_allow_sql` setting in [[Datasette]].

## Applications

- Mapping coordinates to time zones, as in the tutorial example.
- Publishing spatial data queries as a public API built on [[Datasette]].
- Serving location-based lookups backed by a spatial database.

## Related Concepts

## Related Entities

- [[entities/spatialite|SpatiaLite]]
- [[entities/datasette|Datasette]]

## Mentions in Source

- "[Building a location to time zone API with SpatiaLite](https://datasette.io/tutorials/spatialite) is the latest in the official series of tutorials for Datasette." — [[_Inbox/2023-01-15-weeknotes|2023-01-15-weeknotes]]
- "It demonstrates how SpatiaLite can be used to safely build and deploy a geospatial API." — [[_Inbox/2023-01-15-weeknotes|2023-01-15-weeknotes]]