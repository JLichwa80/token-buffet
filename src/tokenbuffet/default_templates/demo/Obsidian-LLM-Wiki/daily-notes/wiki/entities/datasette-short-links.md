---
type: entity
created: 2026-10-21
updated: 2026-10-21
tags: [project]
aliases:
  - "Datasette short links"
sources:
  - "[[sources/2023-09-17-weeknotes-embeddings_c2332f]]"

generation_complete: true
---

# datasette-short-links

## Description

datasette-short-links is an experimental link shortener for [[Datasette]] being built by [[Alex Garcia]]. Working on it revealed that Datasette needed a way to resolve actor IDs into readable names, which led to the `actors_from_ids` plugin hook. The plugin is one of the first consumers of that new hook. It is part of the social features being developed for [[Datasette Cloud]].

## Related Entities

- [[entities/alex-garcia|Alex Garcia]]
- [[entities/datasette-cloud|Datasette Cloud]]

## Related Concepts

## Mentions in Source

- "Alex is using this in datasette-short-links, and I built two plugins to work with the new hook as well:" — [[_Inbox/2023-09-17-weeknotes-embeddings|2023-09-17-weeknotes-embeddings]]