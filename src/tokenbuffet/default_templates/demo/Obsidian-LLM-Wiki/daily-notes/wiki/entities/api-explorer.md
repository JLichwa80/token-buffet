---
type: entity
created: 2026-10-21
updated: 2026-10-21
tags: [other]
aliases:
  - "Datasette API explorer"
sources:
  - "[[sources/2023-08-30-datasette-plus-weeknotes_748a0c]]"

generation_complete: true
---

# API explorer

## Description

The API explorer is a [[Datasette]] feature added during the 1.0 alpha series that lets users browse an instance's API. A security flaw in it exposed the names of databases and tables to unauthenticated users, even on instances protected by authentication. The contents of those tables were not exposed. The flaw was reported as a GitHub security advisory, later assigned CVE-2023-40570, and fixed in Datasette 1.0a4. [[Datasette Cloud]] access logs showed no unauthenticated access to the affected pages before the fix.

## Related Entities

- [[entities/datasette|Datasette]]
- [[entities/datasette-cloud|Datasette Cloud]]
- [[entities/github|GitHub]]

## Related Concepts

- [[concepts/github-security-advisory|GitHub security advisory]]

## Mentions in Source

- "I realized that the API explorer I added in the 1.0 alpha series was exposing the names of databases and tables (though not their actual content) to unauthenticated users, even for Datasette instances that were protected by authentication." — [[_Inbox/2023-08-30-datasette-plus-weeknotes|2023-08-30-datasette-plus-weeknotes]]