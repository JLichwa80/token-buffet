---
created: 2026-10-21
updated: 2026-10-21
sources:
  - "[[sources/2024-02-09-weeknotes_1bab97]]"

generation_complete: true
---

type: concept
created: 2026-10-21
updated: 2026-10-21
sources: ["[[sources/2024-02-09-weeknotes_1bab97]]"]
tags: [idea]
aliases: ["Datasette as a low-cost host", "Datasette hosting"]
---

# Datasette as a cheap deployment platform

## Definition

An idea that treats an existing [[Datasette]] instance as a low-cost host for small, unrelated pieces of infrastructure, beyond its original role for data exploration and publishing.

## Key Characteristics

- Reuses a Datasette instance that is already running, so no separate server is needed for each small service.
- Hosts small, unrelated services (such as proxies) alongside the data Datasette already serves.
- Extends the use of Datasette from data publishing to general-purpose hosting.
- Relies on the Datasette plugin ecosystem to add the functionality of each hosted service.

## Applications

- Running a quick proxy on an existing Datasette instance to serve content that [[Substack]] blocked from GitHub Actions, using [[datasette-proxy-url]].
- Hosting other lightweight helper endpoints on a Datasette instance that already exists, rather than provisioning a new host.

## Related Concepts

- [[concepts/http-basic-authentication|HTTP Basic authentication]]

## Related Entities

- [[entities/datasette|Datasette]]
- [[entities/substack|Substack]]
- [[entities/datasette-proxy-url|datasette-proxy-url]]

## Mentions in Source

- "I solved it by deploying a quick proxy to a Datasette instance I already had up and running, effectively treating Datasette as a cheap deployment platform for random pieces of proxying infrastructure." — [[_Inbox/2024-02-09-weeknotes|2024-02-09-weeknotes]]
- "I built this one because I ran into a bug with Substack where Substack were denying requests to my newsletter’s RSS feed from code running in GitHub Actions!" — [[_Inbox/2024-02-09-weeknotes|2024-02-09-weeknotes]]