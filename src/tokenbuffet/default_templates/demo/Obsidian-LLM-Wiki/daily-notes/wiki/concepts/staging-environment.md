---
type: concept
created: 2026-10-20
updated: 2026-10-20
tags: [idea]
aliases:
  - "Staging"
  - "Staging environment"
sources:
  - "[[sources/2024-07-19-weeknotes_39632e]]"

generation_complete: true
---

# Staging environment

## Definition

A staging environment is a separate deployment environment in which code can be exercised before it reaches production.

## Key Characteristics

- Separate from the production environment, so changes can be tested without affecting live users or the production cluster.
- Allows deployment code to be tested independently, such as the Fly Machines deployment code for Datasette Cloud.
- Often lacks parity with production when hard-coded values (for example, URLs, names, or credentials) are embedded in the code or in CI workflows; making it work can expose and require removing these values.
- Complements automated tests and [[Continuous deployment]] by providing a place to verify changes end to end before release.

## Applications

- Testing [[Fly Machines]] deployment code for [[Datasette Cloud]] before it touches the production cluster.
- Validating changes to [[GitHub Actions]] workflows, which may contain hard-coded values that must be made configurable.
- Providing a robust way to test a batch of waiting [[Datasette Cloud]] features before shipping them. In the source, Willison notes that the hosted service had good tests and continuous deployment but lacked this environment.

## Related Concepts

- [[concepts/continuous-deployment|Continuous deployment]]

## Related Entities

- [[entities/datasette-cloud|Datasette Cloud]]
- [[entities/fly-machines|Fly Machines]]
- [[entities/github-actions|GitHub Actions]]

## Mentions in Source

- "but the thing I’ve been missing is a solid staging environment." — [[_Inbox/2024-07-19-weeknotes|2024-07-19-weeknotes]]
- "The thing that’s been missing is a separate environment where I can exercise my Fly deployment code independently of the production cluster." — [[_Inbox/2024-07-19-weeknotes|2024-07-19-weeknotes]]