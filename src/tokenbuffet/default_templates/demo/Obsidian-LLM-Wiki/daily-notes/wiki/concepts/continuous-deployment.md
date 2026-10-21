---
type: concept
created: 2026-10-20
updated: 2026-10-20
tags: [terminology]
aliases:
  - "CD"
  - "CI/CD"
sources:
  - "[[sources/2024-07-19-weeknotes_39632e]]"

generation_complete: true
---

# Continuous deployment

## Definition

Continuous deployment is the practice of automatically deploying code changes to production once they pass automated checks.

## Key Characteristics

- Deployment to production is automatic and triggered by passing automated tests or checks, with no manual release step.
- Changes reach production soon after they are made, which keeps each change small and easy to review.
- Usually built on a CI/CD pipeline, such as [[GitHub Actions]].
- Depends on a strong automated test suite, since the tests are the gate for production.
- Works best when paired with a [[Staging environment]] that can catch problems before production.

## Applications

- [[Datasette Cloud]] deploys whenever its tests pass.
- The weeknotes describe the existing automatic deployment as a strength of the Datasette Cloud process. A staging environment is meant to complement it.
- The weeknotes also note a gap: a missing staging step, which the author wants in place before deploying more features.

## Related Concepts

- [[concepts/staging-environment|Staging environment]]

## Related Entities

- [[entities/datasette-cloud|Datasette Cloud]]
- [[entities/github-actions|GitHub Actions]]

## Mentions in Source

- "I have great comprehensive tests for it, continuous deployment that deploys when those tests pass and pretty solid internal documentation (mainly spread out across dozens of GitHub Issues)—but the thing I’ve been missing is a solid staging environment." — [[_Inbox/2024-07-19-weeknotes|2024-07-19-weeknotes]]
- "The main reason I’m so keen on the combination of automated tests, GitHub Actions for CI/CD and extensive documentation" — [[_Inbox/2024-07-19-weeknotes|2024-07-19-weeknotes]]