---
type: entity
created: 2026-10-20
updated: 2026-10-20
tags: [other]
aliases:
  - "Fly.io Machines"
sources:
  - "[[sources/2024-07-19-weeknotes_39632e]]"

generation_complete: true
---

# Fly Machines

## Description

Fly Machines is the hosting service on which [[Datasette Cloud]] deploys new [[datasette]] instances. The weeknotes describe it as the target of the most complex deployment code in Datasette Cloud. Willison's [[Staging environment]] was built so that this Fly deployment code could be exercised separately from the production cluster. Much of the work described in the post involved removing hard-coded values that made that separation difficult. Because the deployment code is central to Datasette Cloud, it is a main reason the staging environment was needed.

## Related Entities

- [[entities/datasette-cloud|Datasette Cloud]]
- [[entities/datasette|datasette]]

## Related Concepts

- [[concepts/staging-environment|Staging environment]]

## Mentions in Source

- "This matters because a lot of the most complex code in Datasette Cloud involves deploying new instances of Datasette to Fly Machines." — [[_Inbox/2024-07-19-weeknotes|2024-07-19-weeknotes]]
- "The thing that’s been missing is a separate environment where I can exercise my Fly deployment code independently of the production cluster." — [[_Inbox/2024-07-19-weeknotes|2024-07-19-weeknotes]]