---
type: entity
created: 2026-10-20
updated: 2026-10-21
generation_complete: true
sources:
  - "[[sources/2024-07-02-weeknotes_55c009]]"
  - "[[sources/2023-10-22-weeknotes_1435b6]]"
  - "[[sources/2023-03-22-weeknotes_1bbf6a]]"
tags:
  - "project"
aliases:
  - "Datasette 1.0 release"
---

# Datasette 1.0

## Description

Datasette 1.0 is the planned major release of [[Datasette]], and a stable [[JSON API]] is one of its key components. [[Simon Willison]] and Alex are driving progress toward the release. [[Datasette Cloud]] serves as a real-world consumer that needs a stable API, so the milestone shapes both the API work and the roadmap for Datasette Cloud. Alex documented the final design in GitHub issue #2360 and is implementing it. The plan is to ship the work as an alpha once it is ready to try.

In March 2023, a complete redesign of Datasette's default JSON format landed as a large branch (PR #1999), described as one of the largest changes needed before 1.0. The old format returned dozens of keys with row data as arrays; the new format returns an object with `ok`, `next` and `rows` keys, with optional extras requested through an `_extra` parameter. As of March 2023 the work was unfinished: documentation still needed to be written, and it was unresolved how the change would affect the endpoint that returns results from an arbitrary SQL query.
## Related Entities

- [[entities/datasette|Datasette]]
- [[entities/datasette-cloud|Datasette Cloud]]
- [[entities/simon-willison|Simon Willison]]

## Related Concepts

- [[concepts/json-api|JSON API]]

## Mentions in Source

- "Datasette Cloud needs a stable JSON API, so we’ve been working on finalizing the JSON API that will be included in Datasette 1.0." — [[_Inbox/2024-07-02-weeknotes|2024-07-02-weeknotes]]
- "We worked together on a final design for this which Alex documented in [#2360: Datasette JSON API changes for 1.0](https://github.com/simonw/datasette/issues/2360)." — [[_Inbox/2024-07-02-weeknotes|2024-07-02-weeknotes]]
- "I finally landed [a GIANT branch](https://github.com/simonw/datasette/pull/1999) I’ve been working on for several months now: a complete redesign of Datasette’s default JSON format, one of the largest changes I need to land prior to releasing Datasette 1.0." — [[_Inbox/2023-03-22-weeknotes|2023-03-22-weeknotes]]