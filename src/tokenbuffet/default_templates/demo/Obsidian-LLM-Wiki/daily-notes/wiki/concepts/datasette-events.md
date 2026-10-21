---
type: concept
created: 2026-10-21
updated: 2026-10-21
tags: [idea]
aliases:
  - "analytical events"
sources:
  - "[[sources/2024-02-27-weeknotes-getting-ready-for-nicar_823782]]"

generation_complete: true
---

# Datasette Events

## Definition

Datasette Events is a mechanism introduced in [[Datasette]] 1.0a8 for emitting analytical events. It gives a Datasette instance a built-in way to report analytics-style events, which can then be sent onward to other systems, such as a central analytics instance.

## Key Characteristics

- Introduced as a core mechanism in [[Datasette]] 1.0a8.
- Emits analytical events from a running Datasette instance.
- Serves as the event source that plugins can forward to other instances.
- Was documented by the author in the 1.0a8 release notes.

## Applications

- Forwarding analytical events from one Datasette instance to a central analytics instance, as done by the [[datasette-events-forward]] plugin.
- Running product analytics on a hosted deployment: the mechanism was first used on [[Datasette Cloud]] to analyse Datasette Cloud itself.
- Supporting [[Dogfooding]], where the analytics tooling is the same product being built.

## Related Concepts

- [[concepts/dogfooding|Dogfooding]]

## Related Entities

- [[entities/datasette|Datasette]]
- [[entities/datasette-cloud|Datasette Cloud]]

## Mentions in Source

- "I wrote about the new Datasette Events mechanism in the 1.0a8 release notes." — [[_Inbox/2024-02-27-weeknotes-getting-ready-for-nicar|2024-02-27-weeknotes-getting-ready-for-nicar]]