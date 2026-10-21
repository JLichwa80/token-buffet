---
created: 2026-10-21
updated: 2026-10-21
sources:
  - "[[sources/2023-10-30-weeknotes_d4a215]]"

generation_complete: true
---

type: entity
created: 2026-10-21
updated: 2026-10-21
sources: ["[[sources/2023-10-30-weeknotes_d4a215]]"]
tags: [other]
aliases: ["PMTiles file format", "PMTiles"]
---

# PMTiles

## Description

PMTiles is a single-file archive format for vector tiles, created by [[Protomaps]]. Because it is designed to be read with HTTP range requests, a client fetches only the bytes needed for the current map view, so one large file can be hosted on cloud storage without a tile server. A full world build is about 107 GB, and users can also extract a small custom subset covering one area. The format is commonly used with [[MapLibre GL]] for rendering. The source author served a detailed map of [[Half Moon Bay]] from a PMTiles extract of about 2 MB.

## Related Entities

- [[entities/protomaps|Protomaps]]
- [[entities/maplibre-gl|MapLibre GL]]
- [[entities/half-moon-bay|Half Moon Bay]]

## Related Concepts

## Mentions in Source

- "The Protomaps [PMTiles](https://docs.protomaps.com/pmtiles/) file format lets you bundle together vector tiles in a single file which is designed to be queried using HTTP range header requests." — [[_Inbox/2023-10-30-weeknotes|2023-10-30-weeknotes]]