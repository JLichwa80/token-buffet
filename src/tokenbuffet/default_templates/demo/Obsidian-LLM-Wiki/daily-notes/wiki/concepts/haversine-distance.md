---
type: concept
created: 2026-10-21
sources:
  - "[[sources/2023-12-31-weeknotes_456c53]]"
tags: [terminology]
stub: true
generation_complete: true
---
# haversine distance

> Stub created by the ingest candidate gate (prose+named) — [[sources/2023-12-31-weeknotes_456c53]] names this without treating it. Will be filled by the next ingest of a source that does.

Haversine distance is the great-circle distance between two points on a sphere, computed from their latitude and longitude. In this source it is the function provided by the datasette-haversine plugin. The plugin adds a custom SQL function to Datasette so queries can calculate these distances directly. The datasette-haversine 0.2.1 release is dated 2023-12-29, the last release listed in the source. The source does not explain the formula, so the concept's role here is limited to the plugin's SQL function.

> "**[datasette-haversine 0.2.1](https://github.com/simonw/datasette-haversine/releases/tag/0.2.1)**—2023-12-29  
  Datasette plugin that adds a custom SQL function for haversine distances" — [[sources/2023-12-31-weeknotes_456c53]]
