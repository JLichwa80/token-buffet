---
type: entity
created: 2026-10-21
updated: 2026-10-21
tags: [other]
aliases:
  - "MapLibre"
sources:
  - "[[sources/2023-10-30-weeknotes_d4a215]]"

generation_complete: true
---

# MapLibre GL

## Description

MapLibre GL is a JavaScript library for serving vector maps in the browser. The author used it to render a custom PMTiles-based map of Half Moon Bay, built with [[Vite]] as the build tool. The build is documented in a TIL titled "Serving a custom vector web map using PMTiles and maplibre-gl." In the author's self-hosted mapping setup, MapLibre GL is the rendering layer. It works with the static-hosting approach that [[PMTiles]] enables, with tiles delivered from [[Protomaps]]-style archives.

## Related Entities

- [[entities/pmtiles|PMTiles]]
- [[entities/protomaps|Protomaps]]

## Related Concepts

## Mentions in Source

- "Lots more details of how I built this, including using Vite as a build tool and the [MapLibre GL](https://maplibre.org/) JavaScript library to serve the map, in my TIL [Serving a custom vector web map using PMTiles and maplibre-gl](https://til.simonwillison.net/gis/pmtiles)." — [[_Inbox/2023-10-30-weeknotes|2023-10-30-weeknotes]]