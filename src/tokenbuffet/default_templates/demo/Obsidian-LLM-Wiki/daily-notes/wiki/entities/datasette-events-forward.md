---
type: entity
created: 2026-10-21
updated: 2026-10-21
tags: [project]
aliases:
  - "events-forward plugin"
sources:
  - "[[sources/2024-02-27-weeknotes-getting-ready-for-nicar_823782]]"

generation_complete: true
---

# datasette-events-forward

## Description

datasette-events-forward is a [[Datasette]] plugin that forwards analytical events from one Datasette instance to another. It was released as version 0.1a1 on 2024-02-20. The plugin was built for [[Datasette Cloud]], so that each Datasette Cloud instance could send its analytics to a central analytics instance. The source describes this as dogfooding, because Datasette Cloud uses its own analytics tooling. The plugin depends on the [[Datasette Events]] mechanism, which was introduced in Datasette 1.0a8. Its design is an application of [[Dogfooding]].

## Related Entities

- [[entities/datasette-cloud|Datasette Cloud]]
- [[entities/datasette|Datasette]]

## Related Concepts

- [[concepts/datasette-events|Datasette Events]]
- [[concepts/dogfooding|Dogfooding]]

## Mentions in Source

- "This new plugin was originally built for Datasette Cloud—it forwards analytical events from an instance to a central analytics instance." — [[_Inbox/2024-02-27-weeknotes-getting-ready-for-nicar|2024-02-27-weeknotes-getting-ready-for-nicar]]