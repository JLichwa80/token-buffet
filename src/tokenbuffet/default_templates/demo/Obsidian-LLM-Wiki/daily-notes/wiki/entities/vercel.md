---
type: entity
created: 2026-10-21
updated: 2026-10-21
tags: [organization]
aliases:
  - "Vercel hosting"
sources:
  - "[[sources/2023-05-01-weeknotes_72fe7e]]"

generation_complete: true
---

# Vercel

## Description

Vercel is a hosting and deployment platform. It hosts Simon Willison's [[Today I Learned]] (TIL) site. The platform enforces a 50MB size limit on deployments. Growth in the [[SQLite]] database that stored the [[Social media cards]] screenshots eventually exceeded that limit. Moving image storage out of the deployed database was therefore necessary, which led to the migration to S3.

## Related Entities

- [[entities/sqlite|SQLite]]
- [[entities/today-i-learned|Today I Learned]]

## Related Concepts

- [[concepts/social-media-cards|Social media cards]]

## Mentions in Source

- "Vercel has a 50MB size limit on deployments and the other day the screenshots finally tipped the database over that limit." — [[_Inbox/2023-05-01-weeknotes|2023-05-01-weeknotes]]